# Generated by Django 3.2.4 on 2021-06-14 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('who', '0002_alter_userinfo_login'),
    ]

    operations = [
        migrations.RunSQL('''
        drop table if exists social_auth_association;
        drop table if exists social_auth_association_id_seq;
        drop table if exists social_auth_code;
        drop table if exists social_auth_code_id_seq;
        drop table if exists social_auth_nonce;
        drop table if exists social_auth_nonce_id_seq;
        drop table if exists social_auth_partial;
        drop table if exists social_auth_partial_id_seq;
        drop table if exists social_auth_usersocialauth;
        drop table if exists social_auth_usersocialauth_id_seq;
        delete from auth_permission where content_type_id in (select id from django_content_type where app_label = '{app_label}');
        delete from django_admin_log where content_type_id in (select id from django_content_type where app_label = '{app_label}');
        delete from django_content_type where app_label = '{app_label}';
        delete from django_migrations where app='{app_label}';
        '''.format(app_label='django_social'))
    ]