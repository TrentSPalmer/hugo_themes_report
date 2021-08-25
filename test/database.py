from rank_hugo_themes import (
    engine, Hugothemes,
    Hugothemes_from_gitlab, sessionmaker
)
from sqlalchemy import asc, func


def get_theme_count():
    session = sessionmaker(bind=engine)()
    theme_count = session.query(Hugothemes).count()
    return theme_count


def get_theme_count_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_count_from_gitlab = session.query(Hugothemes_from_gitlab).count()
    return theme_count_from_gitlab


def get_newest_update_time():
    session = sessionmaker(bind=engine)()
    newest_commit_time = session.query(
        Hugothemes.commit_date_in_seconds
    ).order_by(Hugothemes.commit_date_in_seconds.desc()).first()
    return newest_commit_time


def get_newest_update_time_from_gitlab():
    session = sessionmaker(bind=engine)()
    newest_commit_time = session.query(
        Hugothemes_from_gitlab.commit_date_in_seconds
    ).order_by(
        Hugothemes_from_gitlab.commit_date_in_seconds.desc()).first()
    return newest_commit_time


def get_themes_orderedby_cname():
    session = sessionmaker(bind=engine)()
    return session.query(
        Hugothemes).order_by(asc(func.lower(Hugothemes.cname))).all()


def get_themes_as_dicts_of_sortable_columns():
    session = sessionmaker(bind=engine)()
    return [
        {
            'name': x.cname,
            'date': x.commit_date[0:10],
            'stars': str(x.stargazers_count),
            'min_ver': '' if x.min_ver is None else x.min_ver,
            'license': x.theme_license,
        } for x in session.query(Hugothemes).all()]


def get_themes():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes).all()


def get_themes_from_gitlab_table():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes_from_gitlab).all()


def get_themes_from_gitlab_table_by_date():
    session = sessionmaker(bind=engine)()
    return session.query(
        Hugothemes_from_gitlab).order_by(
        Hugothemes_from_gitlab.commit_date_in_seconds).all()


def get_gitlab_themes():
    session = sessionmaker(bind=engine)()
    return session.query(Hugothemes).filter(
        Hugothemes.url.contains("gitlab")).order_by(
        Hugothemes.commit_date_in_seconds).all()
