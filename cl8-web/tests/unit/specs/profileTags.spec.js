import { tagList } from '../../../src/utils'


const profiles = [{
  "tags": [
    {
      "id": 2,
      "slug": "web",
      "name": "web"
    },
  ],
},
{
  "tags": [
    {
      "id": 2,
      "slug": "web",
      "name": "web"
    }
  ]
}]

describe('taglist', () => {
  describe('given a list of profiles', () => {
    it('it returns a list of unique tags', () => {
      const tags = tagList(profiles)
      expect(tags).toHaveLength(1)
      expect(tags[0].id).toBe(2)
      expect(tags[0].slug).toBe('web')
      expect(tags[0].name).toBe('web')
    })
  })
  describe('given a list of profiles with no tags', () => {
    it('should return an empty array', () => {
      const tags = tagList([{},{}])
      expect(tags).toHaveLength(0)
    })
  })
})