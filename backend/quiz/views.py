from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_transcript_api import YouTubeTranscriptApi
#from .utils import get_transcript, generate_quiz_from_text  # assuming these are in utils.py
import openai
openai.api_key = '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'

def generate_quiz_from_text(text, num_questions=5):
    prompt = f"""
    Generate {num_questions} quiz questions from the following lecture transcript:
    
    "{text}"
    
    Each question should be multiple choice with 4 options and indicate the correct answer.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([segment['text'] for segment in transcript])
        return text
    except Exception as e:
        return str(e)


class GenerateQuizView(APIView):
    # def get(self, request):
    #     return Response({"message": "Please use POST with 'video_url' to generate a quiz."})
    def post(self, request):
        video_url = request.data.get("https://youtu.be/yQW21heOYdw?si=81TfJALrQXP9-_Zt")
        if not video_url:
            return Response({"error": "video_url is required"}, status=400)

        try:
            video_id = video_url.split("v=")[-1][:11]  # basic YouTube ID extraction
            transcript = get_transcript(video_id)
            quiz = generate_quiz_from_text(transcript)
            return Response({"quiz": quiz})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
