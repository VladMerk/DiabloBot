import logging

from asgiref.sync import sync_to_async

import plotly.graph_objects as go
from django.db.models import Min
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from users.models import DiscordUser

from .forms import RoleFilterForm

logger = logging.getLogger(__name__)


def index(request):
    users = DiscordUser.objects.all().prefetch_related('roles')
    if request.method == 'POST':
        form = RoleFilterForm(request.POST)
        if form.is_valid():
            start_date = (form.cleaned_data.get('start_date')
                          or DiscordUser.objects.aggregate(min_date=Min('joined_at')).get('min_date'))
            end_date = form.cleaned_data.get('end_date') or timezone.now()

            if r := form.cleaned_data.get('roles'):
                users = users.filter(roles__in=r)

            data = get_user_count_by_date(users, start_date, end_date)
            plot_html = plot_users_graph(data)

        return render(request, 'dashboard/dashboard.html', context={'graph': plot_html, 'form': form})
    else:
        form = RoleFilterForm()
        start_date = users.aggregate(min_date=Min('joined_at')).get('min_date')
        end_date = timezone.now()
        data = get_user_count_by_date(users, start_date, end_date)
        plot_html = plot_users_graph(data)

    return render(request, 'dashboard/dashboard.html', context={'graph': plot_html, 'form': form})


def get_user_count_by_date(users, start_date, end_date):
    dates_added = (users
                   .filter(joined_at__date__gte=start_date, joined_at__date__lte=end_date)
                   .annotate(date_joined_day=TruncDate('joined_at'))
                   .values_list('date_joined_day', flat=True))

    dates_removed = (users
                     .filter(removed_at__date__gte=start_date, removed_at__date__lte=end_date)
                     .annotate(date_removed_day=TruncDate('removed_at'))
                     .values_list('date_removed_day', flat=True))

    all_dates = sorted(set(list(dates_added) + list(dates_removed)))

    added_count = [dates_added.filter(date_joined_day=date).count() for date in all_dates]
    removed_count = [dates_removed.filter(date_removed_day=date).count() for date in all_dates]

    return {
        'dates': all_dates,
        'added_users': added_count,
        'removed_users': removed_count,
    }


def plot_users_graph(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['dates'], y=data['added_users'], name='Добавленные пользователи'))
    fig.add_trace(go.Bar(x=data['dates'], y=data['removed_users'], name='Удаленные пользователи'))

    fig.update_layout(
        title={
            'text': 'Количество пользователей по дням, за период',
            'y': 0.9,
            'x': 0.5,
            'automargin': True,
            'font': {
                'size': 24
            }
        },
        xaxis_title='Days',
        yaxis_title='Количество пользователей',
        barmode='group'
    )
    fig.update_xaxes(tickangle=45)

    return fig.to_html(full_html=False, default_height=700)
