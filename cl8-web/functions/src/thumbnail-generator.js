const spawn = require('child-process-promise').spawn
const path = require('path')
const os = require('os')

const debug = require('debug')('cl8.thumbnail-generator')
const admin = require('firebase-admin')
const gcs = require('@google-cloud/storage')({
  projectId: 'munster-setup',
  keyFilename: './service-account.json'
})

module.exports = ThumbnailGenerator
/**
 * Thumbnail generator. For generating thumbnails of uploaded photos, using
 * ImageMagick.
 * Intended for use in a cloud function
 *
 *
 * @param {Object} config, config object with keys for accessing google cloud services
 * @param {Object} fileObject, an metadata object representing a file just uploaded
 *
 * @returns {Object} with methods to run the import scripts
 */
function ThumbnailGenerator (admin, fileObject) {
  const fileBucket = fileObject.bucket // The Storage bucket that contains the file.
  const filePath = fileObject.name // File path in the bucket.
  const fileName = path.basename(filePath)
  const contentType = fileObject.contentType // File content type.

  const tmpDir = os.tmpdir()
  const tempFilePath = path.join(tmpDir, fileName)

  const THUMB_SMALL = '36x36'
  const THUMB_LARGE = '200x200'

  // // this definitely has a project ID
  // debug('config.serviceAccount.project_id', config.serviceAccount.project_id)
  // // sanity check
  // if (typeof config.serviceAccount.project_id !== 'string') {
  //   throw new Error(`Service Account has no project ID`)
  // }


  // this bucket here, if it's using the admin thing above - SURELY has a project ID, right?
  // const gcs = admin.storage()
  const bucket = gcs.bucket(fileBucket)

  // check if this is a profile photos, with a profile id
  debug('Profile filename ', fileName.split('-'))

  /**
   * Checks that our file is a image suitable for generating
   * thumbnails from
   *
   * @returns {Boolean} True/false based on if whether the objject is suitable for
   * making a thumbnail
   */
  function validateObject () {
    // Exit if this is triggered on a file that is not an image.
    if (!contentType.startsWith('image/')) {
      debug('This is not an image.')
      return false
    }
    // Exit if the image is already a thumbnail.
    if (fileName.startsWith('thumb_')) {
      debug('Already a Thumbnail.')
      return false
    }
    return true
  }

  /**
   * Fetches the image referred to by the metaData, and saves it to
   * the provided path,
   * @param {String} destPath the intendedPath to download to
   * @returns {Promise} downloadFile returns the local path to the objectx
   */
  function fetchImage (fetchPath, destPath) {
    // debug('Object deets', fileObject)
    debug('Fetching image', fetchPath, 'to put at', destPath)

    let downloadPath
    if (fetchPath) {
      downloadPath = fetchPath
    } else {
      downloadPath = filePath
    }
    return bucket
      .file(downloadPath)
      .download({
        destination: destPath
      })
      .then(() => {
        debug('Image downloaded locally to', destPath)
        return destPath
      })
      .catch(err => {
        debug(err)
        return err
      })
  }

  /**
   * Generates thumbnails locally from the file at the path passed in
   *
   * @param {string} origPath where the original file is
   * @returns {Promise} which resolves to exit code of the thumbnail code
   * returns the local path to the newly created thumbnails
   */
  function makeThumbnails (origPath) {
    const ext = path.extname(origPath)
    const baseName = path.basename(origPath, '.png')

    const smallThumbnailPath = `thumb_${baseName}-${THUMB_SMALL}${ext}`
    const largeThumbnailPath = `thumb_${baseName}-${THUMB_LARGE}${ext}`
    // Generate a thumbnail using ImageMagick.
    debug('making thumbnails for', tempFilePath)

    return Promise.all([
      spawn('convert', [
        origPath,
        '-thumbnail',
        `${THUMB_SMALL}>`,
        smallThumbnailPath
      ]),
      spawn('convert', [
        origPath,
        '-thumbnail',
        `${THUMB_LARGE}>`,
        largeThumbnailPath
      ])
    ])
      .then(results => {
        debug('thumbnails created ', results.map(res => res.code))
        return [smallThumbnailPath, largeThumbnailPath]
      })
      .catch(err => {
        debug(err)
        return err
      })
  }

  /**
   * Accepts a path, and uploads the file at that path, returning the HTTP url
   * the files are accessible at
   *
   * @param {String} Path of paths of files
   * @returns {Promise} of signed urls where the uploaded file can be accessed
   */

  function saveThumb (thumbPath) {
    // construct path on cloud storage
    const cloudThumbPath = path.join(filePath, 'thumbnails', thumbPath)
    const metadata = {
      contentType: contentType
    }

    // upload
    return bucket
      .upload(thumbPath, {
        destination: cloudThumbPath,
        metadata: metadata
      })
      .then(uploadResponse => {
        // debug('file uploaded', uploadResponse[0].metadata.mediaLink)
        // return the signedUrl
        const signedUrlconfig = {
          action: 'read',
          expires: '03-01-2500'
        }
        // if this is from the bucket, and I can *download* files, fine,
        // why would the project not be set?
        // debug(uploadResponse[0])

        return uploadResponse[0].getSignedUrl(signedUrlconfig).then(res => {
          // getSignedUrl, returns a string in an Array, like ["somestring"]
          // and we only want the string
          return res[0]
        })
      })
      .catch(err => {
        debug(err)
        return err
      })
  }

  /**
   * Accepts a list of files, and uploaded them, returning the HTTP urls
   * the files are accessible at
   *
   * @param {Array} Array of paths of files
   * @returns {Promise} of signed urls where the uploaded file can be accessed
   */
  function saveThumbs (pathArray) {
    // make our fetching promises, so we can use Promise.all to wait for the
    // results to come back
    const pathPromises = pathArray.map(thumbPath => {
      return saveThumb(thumbPath)
    })

    return Promise.all(pathPromises).then(results => {
      debug(results)
      return results
    })
  }

  /**
   * Accept a profile id for a user, and the photo, creates thumbnails then up dates
   * thumbnail pics for the user
   *
   * @param {any} profileId
   * @param {any} photo
   */
  function createThumbsForProfile (fetchPath, destPath) {
    // do we have a valid object to work with?
    if (!validateObject()) {
      return null
    }
    // begin processing
    return fetchImage(fetchPath, destPath)
      .then(destPath => {
        debug('image fetched', fetchPath)
        return destPath
      })
      .then(destPath => {
        debug('making thumbnails for', destPath)
        return makeThumbnails(destPath)
      })
      .then(thumbs => {
        debug('uploading thumbs', fetchPath)
        return saveThumbs(thumbs)
      })
      .then(thumbUrls => {
        debug('thumbnails saved, at', thumbUrls)
        return thumbUrls
      })
      .catch(err => {
        debug('error')
        return err
      })
  }

  return {
    validateObject,
    fetchImage,
    makeThumbnails,
    saveThumb,
    saveThumbs,
    createThumbsForProfile
  }
}
