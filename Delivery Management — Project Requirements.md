# Delivery Management — Project Requirements

## 1. Project Overview

Develop a web application for managing delivery/trip documentation.

The application will allow drivers to upload information and photographs related to their activities. An owner will be able to consult the complete history, filter records, view photographs, and download documentation.

The application is initially intended for approximately 4 drivers and 1 owner.

The application must be a web application. A native mobile application is not required.

---

# 2. User Roles

The system must support two roles:

## 2.1. Driver

A driver can:

- Identify themselves.
- Create new records.
- Select the type of record.
- Enter the information required for that record type.
- Take photographs using the device camera.
- Select photographs from the device gallery.
- Submit the record.

A driver cannot:

- Edit existing records.
- Delete existing records.
- Modify records after submission.

## 2.2. Owner

The owner can:

- View all records.
- Filter records.
- View record details.
- View associated photographs.
- Download associated photographs/documentation.

---

# 3. Driver Identification

The system must initially allow the driver to identify themselves by selecting their name from a predefined list.

The initial drivers are:

- Driver 1
- Driver 2
- Driver 3
- Driver 4

Username/password authentication is not required for the initial version.

The system must associate every created record with exactly one driver.

---

# 4. Record Types

The system must support exactly these three initial record categories:

- `remito`
- `fuel`
- `general`

The category must be explicitly associated with every record.

The system must reject unsupported categories.

---

# 5. Remito Requirements

A `remito` record must contain:

- Date.
- Loading location (`donde cargan`).
- Destination.
- Company.
- Remito number.
- At least one photograph.
- No more than two photographs.

All required fields must be validated before the record is created.

---

# 6. Fuel Requirements

A `fuel` record must contain:

- Date.
- Liters.
- At least one photograph.
- No more than two photographs.

The liters value must be a valid numeric value.

All required fields must be validated before the record is created.

---

# 7. General Requirements

A `general` record must contain:

- Date.
- Amount.
- At least one photograph.
- No more than two photographs.

The amount must be a valid numeric value.

All required fields must be validated before the record is created.

---

# 8. Photographs

Every record must support photographs.

Requirements:

- Minimum: 1 photograph.
- Maximum: 2 photographs.
- The user must be able to take a photograph using the device camera.
- The user must be able to select a photograph from the device gallery.
- The application must display a preview of selected photographs before submission.
- The application must prevent selecting more than two photographs.
- Only valid image files may be uploaded.
- The system must associate every photograph with its corresponding record.

The actual image files must be stored in file/object storage rather than directly in the main relational record.

---

# 9. Record Data

Every record must contain, at minimum:

- Unique identifier.
- Driver.
- Category.
- Date.
- Creation timestamp.

The creation timestamp must represent when the record was actually created by the system.

The creation timestamp must not depend on the date entered by the driver.

Category-specific information must also be stored according to the selected category.

---

# 10. Data Integrity

The system must guarantee:

- Every record belongs to an existing driver.
- Every record has exactly one category.
- Every record has a valid date.
- Every record has between 1 and 2 photographs.
- Category-specific required information must be present.
- Invalid records must not be persisted.
- A photograph must not be associated with a nonexistent record.
- A record must not reference a nonexistent driver.

---

# 11. Driver Management

The system must provide access to the available drivers so the frontend can display them to the user.

Initially, the system only needs the predefined drivers.

Driver creation, modification, and deletion through the application are not required for the first version.

---

# 12. Record Creation

The system must provide a mechanism for creating a new record.

The creation flow must be:

1. Select driver.
2. Select record category.
3. Display the appropriate form.
4. Enter the required information.
5. Select or capture photographs.
6. Preview photographs.
7. Validate the information.
8. Submit the record.
9. Store the record and photographs.
10. Inform the user whether the operation succeeded or failed.

A successful submission must create a persistent record.

---

# 13. Record History

The owner must be able to access a history containing all created records.

The history must show at least:

- Date.
- Driver.
- Category.

The owner must be able to open an individual record and see its complete information.

---

# 14. History Filters

The owner must be able to filter the history by:

- Driver.
- Category.
- Date.

The system must support combining filters.

Examples:

- All records from Driver 1.
- All fuel records.
- All records from a specific date.
- All remito records from Driver 2.
- All fuel records between two dates.

The system should support date ranges for the date filter.

---

# 15. Record Details

When viewing a specific record, the owner must be able to see:

### Common information

- Record ID.
- Driver.
- Category.
- Date.
- Creation timestamp.

### Remito

- Loading location.
- Destination.
- Company.
- Remito number.
- Photographs.

### Fuel

- Liters.
- Photographs.

### General

- Amount.
- Photographs.

---

# 16. Photograph Viewing

The owner must be able to view all photographs associated with a record.

Photographs must be displayed clearly enough to inspect the uploaded documentation.

If a record contains two photographs, both must be accessible.

---

# 17. Photograph Download

The owner must be able to download photographs associated with a record.

The downloaded file must correspond to the original uploaded photograph.

---

# 18. Error Handling

The application must provide clear feedback when an operation fails.

The system must handle at least:

- Invalid driver.
- Invalid category.
- Missing required fields.
- Invalid numeric values.
- Invalid date.
- More than two photographs.
- No photograph.
- Invalid image file.
- Image upload failure.
- Database failure.
- Record not found.

Internal errors must not expose sensitive implementation details to the user.

---

# 19. Security Requirements

Sensitive configuration must not be included in the source repository.

The following types of information must be kept outside version control:

- Database credentials.
- Supabase credentials.
- API keys.
- Service-role keys.
- Other secrets.

The application must use environment variables for sensitive configuration.

Photographs and documentation should not be publicly accessible without authorization.

---

# 20. Database Requirements

The system must use a relational database.

The database must persist:

- Drivers.
- Records.
- Photograph metadata/references.

There must be a relationship between:

```text
Driver → Records → Photographs
```

Deleting or modifying database entities must not leave invalid references.

Database schema changes must be reproducible through migrations.

---

# 21. Persistence Requirements

Once a record has been successfully created:

- The record must remain available after restarting the application.
- Its photographs must remain available.
- The relationship between the record and its photographs must remain intact.
- The record must appear in the owner's history.

---

# 22. Frontend Requirements

The web interface must:

- Be usable from desktop and mobile browsers.
- Provide simple navigation.
- Clearly distinguish the three record types.
- Display only the fields relevant to the selected category.
- Prevent invalid submissions when possible.
- Provide photograph previews.
- Display loading states during operations.
- Display success/error feedback.
- Prevent accidental submission of incomplete forms.

The driver workflow should require as few steps as reasonably possible.

---

# 23. Responsive Design

The application must work correctly on:

- Desktop browsers.
- Mobile browsers.

The driver interface should prioritize mobile usability because photographs will generally be captured or selected from a mobile device.

---

# 24. Initial Scope Limitations

The first version does NOT require:

- Native Android application.
- Native iOS application.
- Real-time GPS tracking.
- Driver location tracking.
- Real-time vehicle tracking.
- Chat.
- Notifications.
- Payments.
- Billing.
- OCR.
- Automatic document recognition.
- Advanced analytics.
- Reports/statistics.
- Editing existing records.
- Deleting records through the frontend.
- Driver self-registration.
- Password recovery.
- Complex user administration.

These may be added in future versions but are outside the initial scope.

---

# 25. Expected End-to-End Behavior

The complete initial system must support this workflow:

```text
DRIVER

Select driver
      ↓
Select category
      ↓
Fill category-specific information
      ↓
Take/select 1–2 photographs
      ↓
Preview photographs
      ↓
Submit
      ↓
System validates information
      ↓
System stores record
      ↓
System stores photographs
      ↓
System associates photographs with record
      ↓
Success confirmation
```

And:

```text
OWNER

Open history
      ↓
View records
      ↓
Filter by driver/category/date
      ↓
Select record
      ↓
View complete information
      ↓
View photographs
      ↓
Download photographs
```

---

# 26. Acceptance Criteria

The initial version is considered complete only when all of the following are possible:

- [ ] A driver can select their identity.
- [ ] A driver can create a remito record.
- [ ] A driver can create a fuel record.
- [ ] A driver can create a general record.
- [ ] Remito records contain all required remito information.
- [ ] Fuel records contain liters.
- [ ] General records contain amount.
- [ ] Every record requires at least one photograph.
- [ ] No record can contain more than two photographs.
- [ ] Photographs can be captured with the device camera.
- [ ] Photographs can be selected from the gallery.
- [ ] Photographs can be previewed before submission.
- [ ] Records are persisted in the database.
- [ ] Photographs are persisted in storage.
- [ ] Photographs remain associated with their records.
- [ ] The owner can view all records.
- [ ] The owner can filter by driver.
- [ ] The owner can filter by category.
- [ ] The owner can filter by date.
- [ ] Filters can be combined.
- [ ] The owner can view record details.
- [ ] The owner can view associated photographs.
- [ ] The owner can download photographs.
- [ ] Invalid data is rejected.
- [ ] Invalid drivers are rejected.
- [ ] Invalid categories are rejected.
- [ ] Database relationships remain consistent.
- [ ] Sensitive credentials are not stored in the repository.
- [ ] The application works on desktop and mobile browsers.
- [ ] The complete driver → upload → storage → owner history workflow works end-to-end.