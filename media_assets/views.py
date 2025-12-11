from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import MediaAsset, EnvironmentalData
from .forms import MediaAssetForm, EnvironmentalDataForm
from accounts.models import User

# Create your views here.

@login_required
def dashboard_view(request):
    '''main dashboard:show all public media assets and user stats'''
    media_list = MediaAsset.objects.filter(is_public=True)
    query = request.GET.get('q', '')
    if query:
        media_list = media_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    paginator = Paginator(media_list, 12)
    page_number = request.GET.get('page')
    media_assets = paginator.get_page(page_number)

    # User stats
    user_submissions = EnvironmentalData.objects.filter(user=request.user).count()
    recent_activity = EnvironmentalData.objects.filter(user=request.user).order_by('-created_at')[:5]
    alerts = EnvironmentalData.objects.filter(user=request.user, is_approved=False).count()

    return render(request, 'media_assets/dashboard.html',{
        'media_assets': media_assets, 'query': query,
        'user_submissions': user_submissions,
        'recent_activity': recent_activity,
        'alerts': alerts
    })

@login_required
def edit_data_view(request, pk):
    '''edit environmental data submission'''
    data = get_object_or_404(EnvironmentalData, pk=pk)
    if data.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this data.')
        return redirect('media_assets:dashboard')

    if request.method == 'POST':
        form = EnvironmentalDataForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Environmental data updated successfully.')
            return redirect('media_assets:dashboard')
    else:
        form = EnvironmentalDataForm(instance=data)

    return render(request, 'media_assets/edit_data.html',{
        'form': form, 'data': data
    })

@login_required
def delete_data_view(request, pk):
    '''delete environmental data submission'''
    data = get_object_or_404(EnvironmentalData, pk=pk)
    if data.user != request.user and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete this data.')
        return redirect('media_assets:dashboard')

    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Environmental data deleted successfully.')
        return redirect('media_assets:dashboard')

    return render(request, 'media_assets/delete_data.html',{
        'data': data
    })
## admin approval
@login_required
def approve_data_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to approve data.')
        return redirect('media_assets:dashboard')
    
    data = get_object_or_404(EnvironmentalData, pk=pk)
    data.is_approved = True
    data.save()
    messages.success(request, 'Environmental data approved successfully.')
    return redirect('media_assets:dashboard')
@ login_required
def reject_data_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to reject data.')
        return redirect('media_assets:dashboard')
    
    data = get_object_or_404(EnvironmentalData, pk=pk)
    data.is_approved = False
    data.save()
    messages.success(request, 'Environmental data rejected.')
    return redirect('media_assets:dashboard')
    
@login_required
def my_media_view(request):
    '''view for user's own media assets'''
    media_list = MediaAsset.objects.filter(uploaded_by=request.user)
    paginator = Paginator(media_list, 12)
    page_number = request.GET.get('page')
    media_assets = paginator.get_page(page_number)
    return render(request, 'media_assets/my_media.html',{
        'media_assets': media_assets
    })

@login_required
def upload_media_view(request):
    ''' upload media asset'''
    if request.method == 'POST':
        form = MediaAssetForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.uploaded_by = request.user
            media.save()
            messages.success(request, 'Media uploaded successfully.')
            return redirect('media_assets:my_media')
    else:
        form = MediaAssetForm()
    return render(request, 'media_assets/upload_media.html',{
        'form': form
    })


@login_required
def media_detail_view(request,pk):
    '''showcases media details'''
    media = get_object_or_404(MediaAsset, pk=pk)
    ## app specifications
    if not media.is_public and media.uploaded_by != request.user and not request.user.is_admin() and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view this media.')
        return redirect('media_assets:dashboard')

    media.views_count += 1
    media.save(update_fields=['views_count'])
    return render(request, 'media_assets/media_detail.html',{
        'media': media
    })

## edit and delete views
@login_required
def edit_media_view(request, pk):
    '''edit media asset'''
    media = get_object_or_404(MediaAsset, pk=pk)
    if not media.can_edit(request.user):
        messages.error(request, 'You do not have permission to edit this media.')
        return redirect('media_assets:dashboard')

    if request.method == 'POST':
        form = MediaAssetForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated successfully.')
            return redirect('media_assets:media_detail', pk=pk)
    else:
        form = MediaAssetForm(instance=media)

    return render(request, 'media_assets/edit_media.html',{
        'form': form, 'media': media
    })

@login_required
def delete_media_view(request, pk):
    '''delete media asset based of pk'''
    media = get_object_or_404(MediaAsset, pk=pk)
    if not media.can_delete(request.user):
        messages.error(request, "You do not have permission to delete this media.")
        return redirect("media_assets:dashboard")

    if request.method == 'POST':
        media.delete()
        messages.success(request, "Media deleted successfully.")
        return redirect("media_assets:my_media")

    return render(request, 'media_assets/delete_media.html',{
        'media': media
    })

@login_required
def submit_data_view(request):
    '''submit environmental data'''
    if request.method == 'POST':
        form = EnvironmentalDataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Environmental data submitted successfully.')
            return redirect('media_assets:dashboard')
    else:
        form = EnvironmentalDataForm()
    return render(request, 'media_assets/submit_data.html',{
        'form': form
    })

@login_required
def reports_view(request):
    '''view for environmental data reports'''
    data_list = EnvironmentalData.objects.filter(is_approved=True)
    data_type = request.GET.get('data_type')
    location = request.GET.get('location')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if data_type:
        data_list = data_list.filter(data_type=data_type)
    if location:
        data_list = data_list.filter(location__icontains=location)
    if start_date:
        data_list = data_list.filter(date_recorded__date__gte=start_date)
    if end_date:
        data_list = data_list.filter(date_recorded__date__lte=end_date)

    paginator = Paginator(data_list, 20)
    page_number = request.GET.get('page')
    data_list = paginator.get_page(page_number)

    return render(request, 'media_assets/reports.html',{
        'data_list': data_list,
        'is_paginated': data_list.has_other_pages(),
        'page_obj': data_list
    })

@login_required
def charts_view(request):
    '''view for environmental data charts'''
    if not request.user.has_active_premium():
        messages.info(request, 'Charts and analytics are premium features. Upgrade to access visual data insights.')
        return redirect('mpesa:subscription')

    data_list = EnvironmentalData.objects.filter(is_approved=True)
    # Calculate counts for charts
    air_quality_count = data_list.filter(data_type='air_quality').count()
    waste_count = data_list.filter(data_type='waste').count()
    water_count = data_list.filter(data_type='water').count()
    other_count = data_list.filter(data_type='other').count()

    import json
    chart_data = {
        'air_quality': air_quality_count,
        'waste': waste_count,
        'water': water_count,
        'other': other_count
    }

    return render(request, 'media_assets/charts.html',{
        'data_list': data_list,
        'chart_data_json': json.dumps(chart_data)
    })

@login_required
def admin_dashboard_view(request):
    '''admin dashboard view'''
    if not request.user.is_superuser and not (hasattr(request.user, 'user_type') and request.user.user_type == 'admin'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('media_assets:dashboard')

    total_users = User.objects.count()
    total_submissions = EnvironmentalData.objects.count()
    pending_approvals = EnvironmentalData.objects.filter(is_approved=False).count()
    approved_data = EnvironmentalData.objects.filter(is_approved=True).count()
    recent_submissions = EnvironmentalData.objects.order_by('-created_at')[:10]

    return render(request, 'media_assets/admin_dashboard.html',{
        'total_users': total_users,
        'total_submissions': total_submissions,
        'pending_approvals': pending_approvals,
        'approved_data': approved_data,
        'recent_submissions': recent_submissions
    })
