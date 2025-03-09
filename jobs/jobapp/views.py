from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

jobs_data = {
    1:
        {   'id': 1,
            'title': 'Data Scientist',
            'description': 'We are seeking a Data Scientist to analyze complex datasets and build predictive models. Proficiency in Python, R, and machine learning is required.',
            'company': 'Data Insights LLC',
            'salary': 110000
        },
    2:
        {
            'id': 2,
            'title': 'Frontend Developer',
            'description': 'Join our team as a Frontend Developer to create responsive and user-friendly web applications. Experience with React and JavaScript is a must.',
            'company': 'Web Masters Co.',
            'salary': 85000
        },
    3:
        {
            'id': 3,
            'title': 'DevOps Engineer',
            'description': 'We are hiring a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines. Knowledge of AWS, Docker, and Kubernetes is required.',
            'company': 'Cloud Solutions Ltd.',
            'salary': 105000
        },
    4:
        {
            'id': 4,
            'title': 'Product Manager',
            'description': 'We need a Product Manager to oversee the development and launch of new products. Strong communication and project management skills are essential.',
            'company': 'Innovate Tech',
            'salary': 120000
        },
    5:
        {
            'id': 5,
            'title': 'UX/UI Designer',
            'description': 'We are looking for a UX/UI Designer to create intuitive and visually appealing designs. Proficiency in Figma and Adobe XD is required.',
            'company': 'Creative Minds Agency',
            'salary': 90000
        }
}


def _get_next_job_id():
    return max(jobs_data.keys(), default=0) + 1

class JobList(APIView):
    def get(self, request):
        jobs_list = list(jobs_data.values())
        return Response(jobs_list)

    def post(self, request):
        try:
            data = request.data
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        job_id = _get_next_job_id()
        job = {
            'id': job_id,
            'title': data.get('title', 'Default Title'),
            'description': data.get('description', ''),
            'company': data.get('company', ''),
            'salary': data.get('salary', None)
        }
        jobs_data[job_id] = job
        return Response(job, status=201)

class JobDetail(APIView):
    def get(self, request, pk):
        try:
            job = jobs_data[pk]
        except KeyError:
            return Response({"error": "Job not found"}, status=404)
        return Response(job)

    def put(self, request, pk):
        try:
            job = jobs_data[pk]
        except KeyError:
            return Response({"error": "Job not found"}, status=404)

        try:
            data =  data = request.data
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON"}, status=400)

        job.update({
            'title': data.get('title', job.get('title')),
            'description': data.get('description', job.get('description')),
            'company': data.get('company', job.get('company')),
            'salary': data.get('salary', job.get('salary'))
        })
        return Response(job)



    def delete(self, request, pk):
        try:
            del jobs_data[pk]
        except KeyError:
            return Response({"error": "Job not found"}, status=404)
        return Response({}, status=204)