import datetime
import logging

import pandas as pd
import plotly.graph_objects as go
from django.db.models import Min, QuerySet
from django.shortcuts import render
from django.utils import timezone

from users.models import DiscordUser

from .forms import RoleFilterForm

logger = logging.getLogger(__name__)


def index(request):
    users = DiscordUser.objects.all()
    if request.method == "POST":
        form = RoleFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get(
                "start_date"
            ) or DiscordUser.objects.aggregate(min_date=Min("joined_at")).get(
                "min_date"
            )
            end_date = form.cleaned_data.get("end_date") or timezone.now().date()

            if r := form.cleaned_data.get("roles"):
                users = users.filter(roles__in=r)

            data = get_user_count_by_date(users, start_date, end_date)
            plot_html = plot_users_graph(data)

        return render(
            request,
            "dashboard/dashboard.html",
            context={"graph": plot_html, "form": form},
        )
    else:
        form = RoleFilterForm()
        start_date = users.aggregate(min_date=Min("joined_at")).get("min_date")
        end_date = timezone.now()
        data = get_user_count_by_date(users, start_date, end_date)
        plot_html = plot_users_graph(data)

    return render(
        request, "dashboard/dashboard.html", context={"graph": plot_html, "form": form}
    )


def filter_and_group_users(
    users: QuerySet,
    date_field: str,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
):
    users_filtered = users.filter(
        **{f"{date_field}__date__range": [start_date, end_date]}
    ).values("id", date_field)
    users_df = pd.DataFrame(users_filtered)

    if not users_df.get(date_field, pd.DataFrame()).empty:
        users_df[date_field] = pd.to_datetime(users_df[date_field]).dt.date
        users_grouped = users_df.groupby(date_field).agg({"id": "count"}).fillna(0)
        users_grouped.columns = [date_field]
    else:
        start_date = pd.Timestamp(start_date.strftime("%Y-%m-%d"))
        end_date = pd.Timestamp(end_date.strftime("%Y-%m-%d"))

        all_dates = pd.date_range(start_date, end_date, freq="D")
        users_grouped = pd.DataFrame(
            {f"{date_field}": [0] * len(all_dates)}, index=all_dates
        )

    return users_grouped


def get_user_count_by_date(
    users: QuerySet, start_date: datetime.datetime, end_date: datetime.datetime
):
    joined_users_grouped = filter_and_group_users(
        users, "joined_at", start_date, end_date
    )
    removed_users_grouped = filter_and_group_users(
        users, "removed_at", start_date, end_date
    )

    grouped = pd.concat([joined_users_grouped, removed_users_grouped], axis=1)

    return {
        "dates": grouped.index.tolist(),
        "added_users": grouped["joined_at"].tolist(),
        "removed_users": grouped["removed_at"].tolist(),
    }


def plot_users_graph(data):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=data["dates"], y=data["added_users"], name="Добавленные пользователи")
    )
    fig.add_trace(
        go.Bar(x=data["dates"], y=data["removed_users"], name="Удаленные пользователи")
    )

    fig.update_layout(
        title={
            "text": "Количество пользователей по дням",
            "y": 0.9,
            "x": 0.5,
            "automargin": True,
            "font": {"size": 24},
        },
        xaxis_title="Days",
        yaxis_title="Количество пользователей",
        barmode="group",
    )
    fig.update_xaxes(tickangle=45)

    return fig.to_html(full_html=False, default_height=700)
