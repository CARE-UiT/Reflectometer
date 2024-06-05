import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import User, Course, Participant, Session, Response, Curve

# Import CRUD functions
from crud import (
    create_user, get_user, update_user, delete_user,
    create_course, get_course, update_course, delete_course,
    create_participant, get_participant, update_participant, delete_participant,
    create_session, get_session_by_id, update_session, delete_session,
    create_response, get_response, update_response, delete_response,
    create_curve, get_curve, update_curve, delete_curve
)

DATABASE_URL = "sqlite:///:memory:"

class TestCRUDOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)
    
    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.Session.kw['bind'])

    def test_create_user(self):
        create_user(self.session, "test_user", "test@example.com", "hashed_password", "salt")
        user = get_user(self.session, 1)
        self.assertIsNotNone(user)
        self.assertEqual(user.user_name, "test_user")

    def test_update_user(self):
        create_user(self.session, "another_user", "another@example.com", "hashed_password", "salt")
        update_user(self.session, 1, email="new_email@example.com")
        user = get_user(self.session, 1)
        self.assertEqual(user.email, "new_email@example.com")

    def test_delete_user(self):
        create_user(self.session, "delete_user", "delete@example.com", "hashed_password", "salt")
        delete_user(self.session, 1)
        user = get_user(self.session, 1)
        self.assertIsNone(user)

    def test_create_course(self):
        create_user(self.session, "course_owner", "owner@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "test_course", owner.id)
        course = get_course(self.session, 1)
        self.assertIsNotNone(course)
        self.assertEqual(course.name, "test_course")

    def test_update_course(self):
        create_user(self.session, "course_owner", "owner2@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "update_course", owner.id)
        update_course(self.session, 1, name="new_course_name")
        course = get_course(self.session, 1)
        self.assertEqual(course.name, "new_course_name")

    def test_delete_course(self):
        create_user(self.session, "course_owner", "owner3@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "delete_course", owner.id)
        delete_course(self.session, 1)
        course = get_course(self.session, 1)
        self.assertIsNone(course)

    def test_create_participant(self):
        create_user(self.session, "participant_owner", "owner4@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "participant_course", owner.id)
        create_participant(self.session, "participant_name", 1)
        participant = get_participant(self.session, 1)
        self.assertIsNotNone(participant)
        self.assertEqual(participant.name, "participant_name")

    def test_update_participant(self):
        create_user(self.session, "participant_owner", "owner5@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "participant_course2", owner.id)
        create_participant(self.session, "update_participant", 1)
        update_participant(self.session, 1, name="new_participant_name")
        participant = get_participant(self.session, 1)
        self.assertEqual(participant.name, "new_participant_name")

    def test_delete_participant(self):
        create_user(self.session, "participant_owner", "owner6@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "delete_participant_course", owner.id)
        create_participant(self.session, "delete_participant", 1)
        delete_participant(self.session, 1)
        participant = get_participant(self.session, 1)
        self.assertIsNone(participant)

    def test_create_session(self):
        create_user(self.session, "session_owner", "owner7@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "session_course", owner.id)
        create_session(self.session, "session_name", 1)
        session_obj = get_session_by_id(self.session, 1)
        self.assertIsNotNone(session_obj)
        self.assertEqual(session_obj.name, "session_name")

    def test_update_session(self):
        create_user(self.session, "session_owner", "owner8@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "session_course2", owner.id)
        create_session(self.session, "update_session", 1)
        update_session(self.session, 1, name="new_session_name")
        session_obj = get_session_by_id(self.session, 1)
        self.assertEqual(session_obj.name, "new_session_name")

    def test_delete_session(self):
        create_user(self.session, "session_owner", "owner9@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "delete_session_course", owner.id)
        create_session(self.session, "delete_session", 1)
        delete_session(self.session, 1)
        session_obj = get_session_by_id(self.session, 1)
        self.assertIsNone(session_obj)

    def test_create_response(self):
        create_user(self.session, "response_owner", "owner10@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "response_course", owner.id)
        create_session(self.session, "response_session", 1)
        create_participant(self.session, "response_participant", 1)
        create_curve(self.session, b"curve_data", 1, 1)
        create_response(self.session, "what", "when", "thoughts", "feelings", "actions", "consequences", 1, 1, 1)
        response = get_response(self.session, 1)
        self.assertIsNotNone(response)
        self.assertEqual(response.what, "what")

    def test_update_response(self):
        create_user(self.session, "response_owner", "owner11@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "response_course2", owner.id)
        create_session(self.session, "response_session2", 1)
        create_participant(self.session, "response_participant2", 1)
        create_curve(self.session, b"curve_data2", 1, 1)
        create_response(self.session, "what_update", "when", "thoughts", "feelings", "actions", "consequences", 1, 1, 1)
        update_response(self.session, 1, what="new_what")
        response = get_response(self.session, 1)
        self.assertEqual(response.what, "new_what")

    def test_delete_response(self):
        create_user(self.session, "response_owner", "owner12@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "response_course3", owner.id)
        create_session(self.session, "response_session3", 1)
        create_participant(self.session, "response_participant3", 1)
        create_curve(self.session, b"curve_data3", 1, 1)
        create_response(self.session, "what_delete", "when", "thoughts", "feelings", "actions", "consequences", 1, 1, 1)
        delete_response(self.session, 1)
        response = get_response(self.session, 1)
        self.assertIsNone(response)

    def test_create_curve(self):
        create_user(self.session, "curve_owner", "owner13@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "curve_course", owner.id)
        create_session(self.session, "curve_session", 1)
        create_participant(self.session, "curve_participant", 1)
        create_curve(self.session, b"new_curve_data", 1, 1)
        curve = get_curve(self.session, 1)
        self.assertIsNotNone(curve)
        self.assertEqual(curve.data, b"new_curve_data")

    def test_update_curve(self):
        create_user(self.session, "curve_owner", "owner14@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "curve_course2", owner.id)
        create_session(self.session, "curve_session2", 1)
        create_participant(self.session, "curve_participant2", 1)
        create_curve(self.session, b"curve_data_update", 1, 1)
        update_curve(self.session, 1, data=b"updated_curve_data")
        curve = get_curve(self.session, 1)
        self.assertEqual(curve.data, b"updated_curve_data")

    def test_delete_curve(self):
        create_user(self.session, "curve_owner", "owner15@example.com", "hashed_password", "salt")
        owner = get_user(self.session, 1)
        create_course(self.session, "curve_course3", owner.id)
        create_session(self.session, "curve_session3", 1)
        create_participant(self.session, "curve_participant3", 1)
        create_curve(self.session, b"curve_data_delete", 1, 1)
        delete_curve(self.session, 1)
        curve = get_curve(self.session, 1)
        self.assertIsNone(curve)

if __name__ == '__main__':
    unittest.main()
