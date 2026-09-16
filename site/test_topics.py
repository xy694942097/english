import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class TopicTests(unittest.TestCase):
    def test_real_topics_and_recommendations(self):
        course=json.loads((ROOT/'book/course.json').read_text())
        self.assertGreaterEqual(len(course['topics']),5)
        lessons=[]
        for topic in course['topics']:
            self.assertTrue(topic['question'])
            self.assertTrue(topic['lessons'])
            for lesson in topic['lessons']:
                path=ROOT/lesson['path']
                self.assertTrue(path.is_file(),path)
                self.assertIn('##',path.read_text())
                self.assertTrue(lesson['focus'])
                lessons.append(lesson['path'])
        self.assertIn(course['start'],lessons)
        self.assertEqual(len(lessons),len(set(lessons)))

if __name__=='__main__':unittest.main()
