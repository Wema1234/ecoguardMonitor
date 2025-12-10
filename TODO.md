# EcoGuard Monitor Alignment Tasks

## 1. Models
- [ ] Add EnvironmentalData model to media_assets/models.py with fields for environmental metrics (air_quality, waste_levels, water_levels, location, date, etc.)

## 2. Forms
- [ ] Create EnvironmentalDataForm in media_assets/forms.py for submitting environmental data

## 3. Views
- [ ] Add submit_data_view in media_assets/views.py
- [ ] Add reports_view in media_assets/views.py
- [ ] Add charts_view in media_assets/views.py
- [ ] Add admin_dashboard_view in media_assets/views.py
- [ ] Update dashboard_view to show user stats (submissions, alerts, recent activity)

## 4. Templates
- [ ] Create accounts/profile.html
- [ ] Create media_assets/submit_data.html
- [ ] Create media_assets/reports.html
- [ ] Create media_assets/charts.html
- [ ] Create media_assets/admin_dashboard.html
- [ ] Update base.html to include Chart.js

## 5. URLs
- [ ] Update media_assets/urls.py to include new views
- [ ] Update accounts/urls.py to include profile view

## 6. Migrations and Testing
- [ ] Run makemigrations and migrate
- [ ] Test all new views and templates
- [ ] Ensure Bootstrap styling is applied
