import json
import unittest
from app import create_app
from models import db, Language, TranslationStatus, Translation


class TranslationAppTestCase(unittest.TestCase):
    """This class represents the translation app test case"""

    def inserts(self):
        """Do some initial inserts for the test"""
        en = Language(
            id=1,
            language='en'
        )
        self.db.session.add(en)

        es = Language(
            id=2,
            language='es'
        )
        self.db.session.add(es)

        requested = TranslationStatus(
            id=1,
            status='requested'
        )
        self.db.session.add(requested)

        pending = TranslationStatus(
            id=2,
            status='pending'
        )
        self.db.session.add(pending)

        translated = TranslationStatus(
            id=3,
            status='translated'
        )
        self.db.session.add(translated)

        translation = Translation(
            uid='336f7c6064',
            source_language_id=1,
            input_text='hello world',
            target_language_id=2,
            output_text='hola mundo',
            status_id=1
        )
        self.db.session.add(translation)
        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        """Define test variables and initialize app"""
        self.app, _ = create_app(config='config.TestingConfig')
        self.app.app_context().push()
        self.client = self.app.test_client

        self.db = db
        self.db.init_app(self.app)

        self.db.session.commit()
        self.db.drop_all()
        self.db.create_all()

        self.inserts()

    def tearDown(self):
        """Executed after reach test"""
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()

    def test_db(self):
        """Test if the data was correctly inserted in the db"""
        languages = Language.query.all()
        self.assertEqual(isinstance(languages, list), True)
        self.assertEqual(isinstance(languages[0], Language), True)
        t_status = TranslationStatus.query.all()
        self.assertEqual(isinstance(t_status, list), True)
        self.assertEqual(isinstance(t_status[0], TranslationStatus), True)
        translations = Translation.query.all()
        self.assertEqual(isinstance(translations, list), True)
        self.assertEqual(isinstance(translations[0], Translation), True)

    def test_get_home(self):
        """Test homepage"""
        r = self.client().get('/en-es/')
        self.assertEqual(r.status_code, 200)

    def test_post_home(self):
        """Test method not allowed for home"""
        r = self.client().post('/en-es/')
        self.assertEqual(r.status_code, 405)

    def test_no_prefix(self):
        """Test base url without prefix"""
        r = self.client().get('/')
        self.assertEqual(r.status_code, 404)

    def test_get_translations(self):
        """Test method not allowed for translations endpoint"""
        r = self.client().get('/en-es/translations')
        self.assertEqual(r.status_code, 405)

    def test_post_translations(self):
        """Test POST translation"""
        r = self.client().post(
            '/en-es/translations',
            data=json.dumps({'source-text': 'translate this, please'}),
            content_type='application/json'
        )
        data = r.json
        self.assertEqual(r.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertEqual(isinstance(data["uid"], str), True)

    def test_bad_request_translations(self):
        """Test POST translation with wrong json"""
        r = self.client().post(
            '/en-es/translations',
            data=json.dumps({'wrong-key': 'translate this, please'}),
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)

    def test_patch_translations(self):
        """Test PATCH translation"""
        r = self.client().patch('/en-es/translations/336f7c6064/',)
        data = r.json
        self.assertEqual(r.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(isinstance(data["uid"], str), True)
        self.assertEqual(isinstance(data["status"], str), True)
        self.assertEqual(isinstance(data["output_text"], str), True)

    def test_patch_wrong_uid(self):
        """Test PATCH translation with wrong uid"""
        r = self.client().patch('/en-es/translations/xyz/',)
        self.assertEqual(r.status_code, 400)

    def test_delete_translations(self):
        """Test DELETE translation"""
        r = self.client().delete('/en-es/translations/336f7c6064/',)
        data = json.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['uid'], '336f7c6064')
        translation = Translation.query.get('336f7c6064')
        self.assertEqual(translation, None)


if __name__ == "__main__":
    unittest.main()
