import unittest
import iconfonts


class Tests(unittest.TestCase):

    def test_create_fontdict_file(self):
        res = iconfonts.create_fontdict_file("iconfont_sample.css",
                                             'iconfont_sample.fontd')
        self.assertEqual(res, {'icon-plus-circled': 59395, 'icon-spin6': 59393,
                               'icon-doc-text-inv': 59396,
                               'icon-emo-happy': 59392,
                               'icon-comment': 59397, 'icon-users': 59394})

    def test_register(self):
        iconfonts.register('name', 'iconfont_sample.ttf',
                           'iconfont_sample.fontd')
        self.assertEqual(iconfonts._register['name'][0], 'iconfont_sample.ttf')

    def test_icon(self):
        iconfonts.register('name', 'iconfont_sample.ttf',
                           'iconfont_sample.fontd')
        r = iconfonts.icon('icon-comment')
        self.assertEqual(
            "[font=iconfont_sample.ttf]%s[/font]" % (unichr(59397)), r)
        r = iconfonts.icon('icon-comment', 20)
        self.assertEqual(
            "[size=20][font=iconfont_sample.ttf]%s[/font][/size]" %
            (unichr(59397)), r)


if __name__ == '__main__':
    unittest.main()
