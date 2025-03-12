from django.test import TestCase
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Length  # Length를 여기에서 임포트

from django.utils import timezone
from pybo.models import Answer, Question


class AggregateTestCase(TestCase):

    def setUp(self):
        """
        Test setup method to create initial data
        """
        # 질문 3개 생성
        q1 = Question.objects.create(
            subject="Python이란?",
            content="Python은 프로그래밍 언어입니다.",
            create_date=timezone.now(),
        )
        q2 = Question.objects.create(
            subject="Django란?",
            content="Django는 Python 웹 프레임워크입니다.",
            create_date=timezone.now(),
        )
        q3 = Question.objects.create(
            subject="Java란?",
            content="Java는 객체 지향 언어입니다.",
            create_date=timezone.now(),
        )

        # 각 질문에 대한 답변 생성
        Answer.objects.create(
            question=q1,
            content="Python은 매우 유용합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q1,
            content="Python은 쉽고 강력합니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q2,
            content="Django는 빠르고 확장성이 좋습니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 크로스 플랫폼에서 사용됩니다.",
            create_date=timezone.now(),
        )
        Answer.objects.create(
            question=q3,
            content="Java는 많은 라이브러리와 도구를 지원합니다.",
            create_date=timezone.now(),
        )

    # def test_count_answers(self):
    #     """
    #     Test for Count aggregation on answers
    #     """
    #     result = Answer.objects.aggregate(total_answers=Count("id"))
    #     # SQL 쿼리:
    #     # SELECT COUNT(id) AS total_answers FROM Answer;
    #     print(result)
    #     self.assertEqual(result["total_answers"], 5)

    def test_sum_answer_ids(self):
        """
        Test for Sum aggregation on answer ids
        """
        result = Answer.objects.aggregate(Sum("id"))
        # SQL 쿼리:
        # SELECT SUM(id) FROM Answer;
        print(result)
        self.assertEqual(result["id__sum"], 15)

    def test_avg_answer_ids(self):
        """
        Test for Avg aggregation on answer ids
        """
        result = Answer.objects.aggregate(Avg("id"))
        # SQL 쿼리:
        # SELECT AVG(id) FROM Answer;
        self.assertEqual(result["id__avg"], 3)

    def test_min_answer_create_date(self):
        """
        Test for Min aggregation on the answer's create_date
        """
        query_set = Answer.objects.aggregate(Min("create_date"))
        # SQL 쿼리:
        # SELECT MIN(create_date) FROM Answer;
        print("SQL Query:", Answer.objects.all().query)  # SQL 쿼리 출력

        self.assertIsNotNone(query_set["create_date__min"])

    def test_max_answer_create_date(self):
        """
        Test for Max aggregation on the answer's create_date
        """
        query_set = Answer.objects.aggregate(Max("create_date"))
        # SQL 쿼리:
        # SELECT MAX(create_date) FROM Answer;
        print("SQL Query:", Answer.objects.all().query)  # SQL 쿼리 출력

        self.assertIsNotNone(query_set["create_date__max"])

    def test_aggregate_multiple_fields(self):
        """
        Test multiple aggregation functions together
        """
        result = Answer.objects.aggregate(
            total_answers=Count("id"),
            avg_answers=Avg("id"),
            max_answer_time=Max("create_date"),
        )
        # SQL 쿼리:
        # SELECT COUNT(id) AS total_answers, AVG(id) AS avg_answers, MAX(create_date) AS max_answer_time
        # FROM Answer;
        self.assertEqual(result["total_answers"], 5)
        self.assertEqual(result["avg_answers"], 3)

    def test_aggregate_on_question(self):
        """
        Test aggregate on Question model, such as counting answers per question
        """
        result = Question.objects.annotate(answer_count=Count("answer")).aggregate(
            total_answers=Sum("answer_count")
        )
        # SQL 쿼리:
        # SELECT SUM(answer_count) AS total_answers
        # FROM (SELECT COUNT(answer.id) AS answer_count FROM Question
        #       LEFT JOIN Answer ON Question.id = Answer.question_id
        #       GROUP BY Question.id) AS subquery;
        self.assertEqual(result["total_answers"], 5)

    def test_avg_question_content_length(self):
        """
        Test for average length of question content
        """
        result = Question.objects.annotate(content_length=Length("content")).aggregate(
            avg_content_length=Avg("content_length")
        )
        # SQL 쿼리:
        # SELECT AVG(LENGTH(content)) AS avg_content_length FROM Question;
        self.assertGreater(result["avg_content_length"], 0)
