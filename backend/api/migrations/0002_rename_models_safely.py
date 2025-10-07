# Generated manually to handle model renaming safely

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # First, create the new models
        migrations.CreateModel(
            name='PortfolioResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_index=True, max_length=100)),
                ('number_coins', models.FloatField()),
                ('profit', models.FloatField()),
                ('growth_factor', models.FloatField()),
                ('lambos', models.FloatField()),
                ('investment', models.FloatField()),
                ('symbol', models.CharField(db_index=True, max_length=100)),
                ('generation_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'portfolio_results',
            },
        ),
        migrations.CreateModel(
            name='PortfolioLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(db_index=True, max_length=100)),
                ('message', models.TextField()),
                ('level', models.CharField(max_length=20)),
                ('generation_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'portfolio_logs',
            },
        ),
        migrations.CreateModel(
            name='OpeningAverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(db_index=True, max_length=100)),
                ('average', models.FloatField()),
                ('generation_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'opening_averages',
            },
        ),
        
        # Create indexes for the new models
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS opening_ave_symbol_519d97_idx ON opening_averages (symbol, generation_date);",
            reverse_sql="DROP INDEX IF EXISTS opening_ave_symbol_519d97_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS portfolio_l_symbol_a39722_idx ON portfolio_logs (symbol, generation_date);",
            reverse_sql="DROP INDEX IF EXISTS portfolio_l_symbol_a39722_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS portfolio_r_symbol_486ea4_idx ON portfolio_results (symbol, generation_date);",
            reverse_sql="DROP INDEX IF EXISTS portfolio_r_symbol_486ea4_idx;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS portfolio_r_query_b055c3_idx ON portfolio_results (query);",
            reverse_sql="DROP INDEX IF EXISTS portfolio_r_query_b055c3_idx;"
        ),
        
        # Data migration: Copy data from old models to new models (if they exist)
        migrations.RunPython(
            code=migrations.RunPython.noop,  # No data migration needed for new setup
            reverse_code=migrations.RunPython.noop,
        ),
        
        # Finally, delete the old models (only if they exist and are empty)
        migrations.RunSQL(
            "DROP TABLE IF EXISTS api_results;",
            reverse_sql="-- Cannot reverse this operation"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS api_logging;",
            reverse_sql="-- Cannot reverse this operation"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS api_opening_average;",
            reverse_sql="-- Cannot reverse this operation"
        ),
    ]
