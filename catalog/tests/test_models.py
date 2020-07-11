from django.test import TestCase
from catalog.models import Author

# Put your test's there

class MyTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false")
        self.assertFalse(False)
        pass

    def test_false_is_true(self):
        print("Method: test_false_is_true")
        self.assertTrue(False)
        pass

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two")
        self.assertEqual(1+1,2)
        pass

class AuthorTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
        pass

    def test_first_name(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')
        pass

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')
        pass

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)
        pass

    def test_last_name(self):
        author = Author.objects.get(id=1)
        field_label=author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
        pass

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))
        pass

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/authors/1')
        pass