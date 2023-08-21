from itertools import count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import *
from .models import *
from .functions import *


@login_required
def home(request):
    emptyBlogs = []
    completedBlogs = []
    monthCount = 0
    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSection.objects.filter(blog=blog)
        if sections.exists():
            # Calculate Blog Words
            blogWords = 0
            for section in sections:
                blogWords += int(section.wordCount)
                monthCount += int(section.wordCount)
            blog.wordCount = str(blogWords)
            blog.save()

            completedBlogs.append(blog)
        else:
            emptyBlogs.append(blog)

    allowance = checkCountAllowance(request.user.profile)

    context = {'numBlogs': len(completedBlogs), 'monthCount': request.user.profile.monthlyCount, 'countReset': '11 July 2023',
               'emptyBlogs': emptyBlogs, 'completedBlogs': completedBlogs, 'allowance': allowance}
    return render(request, 'dashboard/home.html', context)


@login_required
def profile(request):

    context = {}
    profile = request.user.profile
    user = request.user

    if request.method == 'GET':
        form = ProfileForm(instance=profile, user=user)
        image_form = ProfileImageForm(instance=profile)
        context = {'form': form, 'image_form': image_form}
        return render(request, 'dashboard/profile.html', context)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=user)
        image_form = ProfileImageForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        if image_form.is_valid:
            image_form.save()
            return redirect('profile')

    return render(request, 'dashboard/profile.html', context)


@login_required
def blogTopic(request):
    context = {}

    if request.method == 'POST':
        blogIdea = request.POST['blogIdea']
        request.session['blogIdea'] = blogIdea

        keywords = request.POST['keywords']
        request.session['keywords'] = keywords

        audience = request.POST['audience']
        request.session['audience'] = audience

        blogTopics = generateBlogTopicIdeas(blogIdea, audience, keywords)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog-section')
        else:
            messages.error(
                request, 'Oops, could not generate any blog ideas, try again!!')
            return redirect('blog-topic')

    return render(request, 'dashboard/blog-topic.html', context)


@login_required
def blogSection(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request, 'Start by Creating blog topic ideas')
        return redirect('blog-topic')

    context = {}
    context['blogTopics'] = request.session['blogTopics']

    return render(request, 'dashboard/blog-section.html', context)


@login_required
def deleteBlogTopic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect('dashboard')
        else:
            messages.error(
                request, 'Oops, Access denied!!')
            return redirect('dashboard')
    except:
        messages.error(
            request, 'Oops, Blog not found!!')
        return redirect('dashboard')


@login_required
def saveBlogTopic(request, blogTopic):
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session and 'blogTopics' in request.session:
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session['blogIdea'],
            keywords=request.session['keywords'],
            audience=request.session['audience'],

            # Related Field
            profile=request.user.profile
        )
        blog.save()

        blogTopics = request.session['blogTopics']
        blogTopics.remove(blogTopic)
        request.session['blogTopics'] = blogTopics

        return redirect('blog-section')
    else:
        return redirect('blog-topic')


@login_required
def useBlogTopic(request, blogTopic):
    context = {}
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session:
        # Save the blog first
        blog = Blog.objects.create(
            title=blogTopic,
            blogIdea=request.session['blogIdea'],
            keywords=request.session['keywords'],
            audience=request.session['audience'],

            # Related Field
            profile=request.user.profile
        )
        blog.save()

        blogSections = generateBlogSectionTitles(
            blogTopic, request.session['audience'], request.session['keywords'])
    else:
        return redirect('blog-topic')

    if len(blogSections) > 0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
    else:
        messages.error(
            request, 'Oops, You beat the AI, try again!!')
        return redirect('blog-topic')

    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                # Generate blog details
                section = generateBlogSectionDetails(
                    blogTopic, val, request.session['audience'], request.session['keywords'], request.user.profile)

                # Create Database Record
                blogSec = BlogSection.objects.create(
                    title=val,
                    body=section,
                    blog=blog
                )
                blogSec.save()

        return redirect('view-generated-blog', slug=blog.slug)

    return render(request, 'dashboard/select-blog-section.html', context)


@login_required
def createBlogFromTopic(request, uniqueId):
    context = {}

    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(
            request, 'Oops, Blog not found!!')
        return redirect('dashboard')

    blogSections = generateBlogSectionTitles(
        blog.title, blog.audience, blog.keywords)

    if len(blogSections) > 0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
    else:
        messages.error(
            request, 'Oops, You beat the AI, try again!!')
        return redirect('blog-topic')

    if request.method == 'POST':
        for val in request.POST:
            if not 'csrfmiddlewaretoken' in val:
                # Generate blog details
                section = generateBlogSectionDetails(
                    blog.title, val, blog.audience, blog.keywords, request.user.profile)

                # Create Database Record
                blogSec = BlogSection.objects.create(
                    title=val,
                    body=section,
                    blog=blog
                )
                blogSec.save()

        return redirect('view-generated-blog', slug=blog.slug)

    return render(request, 'dashboard/select-blog-section.html', context)


@login_required
def generatedBlog(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(
            request, 'Oops, Something went Wrong!!')
        return redirect('blog-topic')

    # Fetch the Created Sections for the Blog
    blogSections = BlogSection.objects.filter(blog=blog)
    print('BLOGSECTIONS:', blogSections)

    context = {'blog': blog, 'blogSections': blogSections}

    return render(request, 'dashboard/generated-blog.html', context)


@login_required
def billing(request):
    context = {}
    return render(request, 'dashboard/billing.html', context)
