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

    # def test_value(self):
    #     ## SQL 쿼리:
    #     ## SELECT subject, content  FROM Answer;
    #     ## 딕셔너리 형태로 반환
    #     result = Question.objects.values("subject", "content")
    #     result = Question.objects.all().values()  # 딕셔너리
    #     result = Question.objects.all().values_list()  # 튜플

    #     # 관련 테입즐 필드 조회(포오린키 조회)

    #     # SELECT Answer.id, Question.subject, Answer.content
    #     # FROM Answer
    #     # JOIN Question ON Answer.question_id = Question.id;

    #     #SELECT "pybo_answer"."id", "pybo_question"."subject", "pybo_answer"."content"
    #     #FROM "pybo_answer" INNER JOIN "pybo_question" ON ("pybo_answer"."question_id" = "pybo_question"."id")

    #     query_set = Answer.objects.values("id", "question__subject", "content")
    #     print(query_set.query)

    def test_filter(self):

        # SELECT * FROM Question WHERE id = 1;

        # 1. 특정 ID의 질문 조회
        query = Question.objects.filter(id=1)
        # print(query.query)

        # 2. 특정 제목을 가진 질문 조회
        # SELECT * FROM Question WHERE subject = 'Django란?';
        query = Question.objects.filter(subject="Django란?")
        # print(query)

        # 3. 특정 내용이 포함된 질문 조회 (icontains)
        # SELECT * FROM Question WHERE content LIKE '%Python%';
        query = Question.objects.filter(content__icontains="Python").values()
        # print(query)

        # 4. 날짜 형 조회

        # query = Question.objects.filter(create_date__gt=datetime(2024, 1, 1))
        # print(query)

        # 5. 숫자 필터링
        # lt < 5 , lte <=5 , gt > 5,gte >=5
        # SELECT * FROM Question WHERE id < 5;

        query = Question.objects.filter(id__lt=5)  # id < 5
        # print(query)

        # 특정 ID 사이의 질문 조회 (between)
        # SELECT * FROM Question WHERE id BETWEEN 1 AND 5;
        query = Question.objects.filter(id__range=(1, 5))  # id < 5
        # print(query)

        # 2025년 1월 1일과 2025년 3월 14일 사이에 생성된 질문
        query = Question.objects.filter(create_date__range=("2025-01-01", "2025-03-14"))
        # print(query)

        # 제목이 'Django란?'이고, 내용에 'MTV'가 포함된 질문
        # SELECT * FROM Question WHERE subject = 'Django란?' AND content LIKE '%MTV%';
        query = Question.objects.filter(
            subject="Django란?", content__icontains="Django"
        )  # dev_2
        # print(query)

        # 제목이 'Django란?'이거나 'Python이란?'인 질문 (OR 조건)
        from django.db.models import Q

        # SELECT * FROM Question WHERE subject = 'Django란?' OR subject = 'Python이란?';
        query = Question.objects.filter(
            Q(subject="Django란?") | Q(subject="Python이란?")
        )  # dev_2
        # print(query)

        # 정렬
        # SELECT * FROM Question ORDER BY create_date DESC LIMIT 2;
        query = Question.objects.order_by("-id").values()[:2]
        # print(query)

        # null 처리
        # query = Question.objects.filter(answer__isnull=True)
        # print(query)

        if Question.objects.filter(subject="Django란?").exists():
            print("해당 질문이 존재합니다.")

    # annotate @, aggregate
    def test_annotate(self):
        pass

    def test_aggregate(self):
        pass

    # def test_sum_answer_ids(self):
    #     """
    #     Test for Sum aggregation on answer ids
    #     """
    #     result = Answer.objects.aggregate(Sum("id"))
    #     # SQL 쿼리:
    #     # SELECT SUM(id) FROM Answer;
    #     print(result)
    #     self.assertEqual(result["id__sum"], 15)
