# from unittest import TestCase
#
# from apps.news.models import News
#
#
# class CompanyListViewTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 companies for pagination tests
#         number_of_news = 3
#
#         for news_num in range(number_of_news):
#             News.objects.create(
#                 headline=f'test news {news_num}',
#                 content=f'Date the news was last modified: 2022-06-10 15:30:23.738493+00:00 {news_num}',
#                 author=
#                 category=
#             )
#
#     def test_view_url_exists_at_desired_location(self):
#         resp = self.client.get('')
#         self.assertEqual(resp.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         resp = self.client.get(reverse('home'))
#         self.assertEqual(resp.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         resp = self.client.get(reverse('home'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'home.html')
#
#     def test_pagination_is_two(self):
#         resp = self.client.get(reverse('home'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue('is_paginated' in resp.context)
#         self.assertTrue(resp.context['is_paginated'] == True)
#         self.assertTrue(len(resp.context['company_list']) == 2)
#
#     def test_lists_all_companies(self):
#         # Get second page and confirm it has (exactly) remaining 1 items
#         resp = self.client.get(reverse('home') + '?page=2')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue('is_paginated' in resp.context)
#         self.assertTrue(resp.context['is_paginated'] == True)
#         self.assertTrue(len(resp.context['company_list']) == 1)
#
#
# class CompanyDetailViewTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         # Create 3 companies for pagination tests
#         number_of_companies = 3
#         for company_num in range(number_of_companies):
#             Company.objects.create(
#                 name='test company %s' % 3,
#                 description="ggfgfggfgfgfggfgfggf jdhhdhdhdh hhhh %s" % 3,
#                 position_person='manager %s' % 3,
#                 contact_person='fg dfg ggg %s' % 3,
#                 address='gdfdf gdfgdgd gdgdggd %s' % 3,
#                 )
#
#     def test_view_url_exists_at_desired_location(self):
#         resp = self.client.get('/company-detail/1')
#         self.assertEqual(resp.status_code, 200)
#
#     # def test_view_url_accessible_by_name(self):
#     #     resp = self.client.get('company_detail')
#     #     self.assertEqual(resp.status_code, 200)
#     #
#     # def test_view_uses_correct_template(self):
#     #     resp = self.client.get('company_detail')
#     #     self.assertEqual(resp.status_code, 200)
#     #     self.assertTemplateUsed(resp, 'company_detail.html')
