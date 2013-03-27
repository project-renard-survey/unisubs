import codecs
import os

from apps.webdriver_testing.webdriver_base import WebdriverTestCase
from apps.webdriver_testing.pages.site_pages import video_page
from apps.webdriver_testing.pages.site_pages import video_language_page
from apps.webdriver_testing import data_helpers
from apps.webdriver_testing.data_factories import UserFactory
from apps.webdriver_testing.data_factories import VideoUrlFactory
from apps.webdriver_testing.pages.editor_pages import subtitle_editor
from apps.webdriver_testing.pages.editor_pages import unisubs_menu 
from apps.webdriver_testing.data_factories import TeamVideoFactory
from apps.webdriver_testing.data_factories import TeamMemberFactory
from apps.webdriver_testing.data_factories import WorkflowFactory


class TestCaseTeamSubtitles(WebdriverTestCase):
    """TestSuite for download subtitles from the video's lanugage page   """
    NEW_BROWSER_PER_TEST_CASE = False

    @classmethod
    def setUpClass(cls):
        super(TestCaseTeamSubtitles, cls).setUpClass()
        cls.data_utils = data_helpers.DataHelpers()
        cls.menu = unisubs_menu.UnisubsMenu(cls)
        cls.user = UserFactory.create()
        cls.team = TeamMemberFactory.create(team__workflow_enabled=True,
                                            team__translate_policy=20,
                                            team__subtitle_policy=20,
                                            user = cls.user,
                                            ).team
        cls.team_workflow = WorkflowFactory(team = cls.team,
                                            autocreate_subtitle=True,
                                            autocreate_translate=True,
                                            approve_allowed = 10,
                                            review_allowed = 10,
                                           )


        cls.video_pg = video_page.VideoPage(cls)
        cls.video_language_pg = video_language_page.VideoLanguagePage(cls)
        cls.subs_data_dir = os.path.join(os.getcwd(), 'apps', 
            'webdriver_testing', 'subtitle_data')

    def tearDown(self):
        self.browser.get_screenshot_as_file('MYTMP/%s.png' % self.id())


    def test_delete_source_forks_translations(self):
        """Deleting source forks translations and new source uploads not blocked.

        """
        sub_file = os.path.join(self.subs_data_dir, 'Timed_text.en.srt')
        video = VideoUrlFactory().video
        orig_data = {'language_code': 'en',
                     'video': video.pk,
                     'primary_audio_language_code': 'en',
                     'draft': open(sub_file),
                     'is_complete': True,
                     'complete': 1,
                    }
        self.data_utils.upload_subs(video, orig_data)
        self.video_language_pg.open_video_lang_page(video.video_id, 'en')


        translation = os.path.join(self.subs_data_dir, 'Timed_text.sv.dfxp')
        trans_data = {'language_code': 'sv',
                      'video': video.pk,
                      'from_language_code': 'en',
                      'draft': open(translation),
                      'is_complete': True,
                      'complete': 1,
                     }
        self.data_utils.upload_subs(video, trans_data)
        TeamVideoFactory.create(
            team=self.team, 
            video=video, 
            added_by=self.user)

        self.video_language_pg.open_video_lang_page(video.video_id, 'sv')
        self.assertIn('from English', self.video_language_pg.view_notice())
        self.video_language_pg.log_in(self.user.username, 'password')
        self.video_language_pg.open_video_lang_page(video.video_id, 'en')
        self.video_language_pg.unpublish(delete=True)

        #sl = video.subtitle_language('en')
        #sl.unpublish(delete=True)
        #sl.save()
        #self.video_language_pg.open_video_lang_page(video.video_id, 'sv')
        sl_sv = video.subtitle_language('sv')
        sub_file = os.path.join(self.subs_data_dir, 'srt-full.srt')
        video = VideoUrlFactory().video
        orig_data = {'language_code': 'en',
                     'video': video.pk,
                     'draft': open(sub_file),
                     'is_complete': True,
                     'complete': 1,
                    }

        self.data_utils.upload_subs(video, orig_data)
        self.logger.info('SV IS_FORKED %s' % sl_sv.is_forked)
        self.assertTrue(sl_sv.is_forked)




