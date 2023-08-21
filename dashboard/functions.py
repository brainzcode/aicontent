import os
import openai
from django.conf import settings

# Load your API key from an environment variable or secret management service
openai.api_key = settings.OPENAI_API_KEY


def generateBlogTopicIdeas(topic, audience, keywords):
    blog_topics = []

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate 6 Blog Topic Ideas on the following Topic: {}\nAudience: {}\nKeywords: {}\n*".format(
            topic, audience, keywords),
        temperature=1,
        max_tokens=256,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    blog_list = res.split('*')
    if len(blog_list) > 0:
        for blog in blog_list:
            blog_topics.append(blog)
    else:
        return []

    return blog_topics


def generateBlogSectionTitles(topic, audience, keywords):
    blog_topics = []

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate adequate blog section titles for the provided blog topic, audience, and keywords: {}\nAudience: {}\nKeywords: {}\n*".format(
            topic, audience, keywords),
        temperature=1,
        max_tokens=256,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    blog_list = res.split('*')
    if len(blog_list) > 0:
        for blog in blog_list:
            blog_topics.append(blog)
    else:
        return []

    return blog_topics


def generateBlogSectionDetails(blogTopic, sectionTopic, audience, keywords, profile):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate detailed blog section write up for the following blog section heading, using the blog title, audience, blog section heading and keywords provided.\nBlog Title: {}\nBlog Section Heading: {}\nAudience: {}\nKeywords:  {}\n\n".format(
            blogTopic, sectionTopic, audience, keywords),
        temperature=1,
        max_tokens=500,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
            if not res == '':
                cleanedRes = res.replace('\n', '<br>')
                if profile.monthlyCount:
                    oldCount = int(profile.monthlyCount)
                else:
                    oldCount = 0

                oldCount += len(cleanedRes.split(' '))
                profile.monthlyCount = str(oldCount)
                profile.save()
                return cleanedRes
            else:
                return ''
        else:
            return ''
    else:
        return ''


def checkCountAllowance(profile):
    if profile.subscribed:
        type = profile.subscriptionType
        if type == 'free':
            max_limit = 5000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                True
        elif type == 'starter':
            max_limit = 40000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                True
        elif type == 'advanced':
            return True
    else:
        max_limit = 5000
        if profile.monthlyCount:
            if int(profile.monthlyCount) < max_limit:
                return True
            else:
                return False
        else:
            True
