---
title: "schema"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/schema"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  // This is your Prisma schema file,
  // learn more about it in the docs: https://pris.ly/d/prisma-schema

// Looking for ways to speed up your queries, or scale easily with your serverless or edge functions?
// Try Prisma Accelerate: https://pris.ly/cli/accelerate-init

generator client {
provider = "prisma-client"
output = "../generated/prisma"
engineType = "library"
}

datasource db {
provider = "postgresql"
schemas = ["base", "billing", "seq"]
}

model User {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
email String @unique @db.VarChar(255)
passwordHash String @map("password_hash") @db.VarChar(255)
username String? @unique @db.VarChar(100)
isAdmin Boolean @default(false) @map("is_admin")
isInstructor Boolean @default(false) @map("is_instructor")
createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz
updatedAt DateTime @default(now()) @updatedAt @map("updated_at") @db.Timestamptz

    profile             Profile?
    address             Address?
    coursesAsInstructor Course[]            @relation("CourseInstructor")
    enrollments         Enrollment[]
    lessonProgress      LessonProgress[]
    certificates        Certificate[]
    eventsAsHost        Event[]             @relation("EventHost")
    invoices            Invoice[]
    eventRegistrations  EventRegistration[]
    affiliate           Affiliate?
    referredBy          Referral[]
    shares              Share[]
    bookmarks           Bookmark[]
    bookmarkFolders     BookmarkFolder[]
    views               View[]
    likes               Like[]
    ratings             Rating[]
    posts               Post[]
    comments            Comment[]
    assets              Asset[]
    activities          Activity[] // Activities created by this user
    following           Follow[]            @relation("UserFollowing") // Users this user follows
    followers           Follow[]            @relation("UserFollowers") // Users who follow this user
    notifications       Notification[] // Notifications received by this user

    @@map("users")
    @@schema("base")

}

enum Gender {
male
female
other
prefer_not_to_say

    @@schema("base")

}

model Profile {
id String @id @db.Uuid
fullName String @map("full_name") @db.VarChar(255)
gender Gender? @map("gender")
nationality String? @map("nationality") @db.VarChar(50)
phone String? @unique @map("phone") @db.VarChar(20)
phoneVerifiedAt DateTime? @map("phone_verified_at") @db.Timestamptz
bio String?
dateOfBirth DateTime? @map("date_of_birth") @db.Date
avatarUrl String? @map("avatar_url")
isProfileComplete Boolean @default(false) @map("is_profile_complete")
createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz
updatedAt DateTime @default(now()) @updatedAt @map("updated_at") @db.Timestamptz

    user User @relation(fields: [id], references: [id], onDelete: Cascade)

    @@map("profiles")
    @@schema("base")

}

enum AddressType {
profile
billing
shipping
office

    @@schema("base")

}

model Address {
id String @id @default(uuid())
userId String @unique @db.Uuid

    // Canonical
    countryCode String  @db.Char(2) // ISO 3166-1 alpha-2 (SA, AE, US)
    city        String?
    postalCode  String?

    // Free-form (most important)
    addressLine1 String  @map("address_line_1")
    addressLine2 String? @map("address_line_2")

    // Optional structured fields
    state        String?
    region       String?
    district     String?
    neighborhood String?

    // Metadata
    type      AddressType @default(profile)
    isDefault Boolean     @default(false)

    // Geocoding
    latitude  Float?
    longitude Float?

    createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz
    updatedAt DateTime @updatedAt @map("updated_at") @db.Timestamptz

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([countryCode])
    @@map("addresses")
    @@schema("base")

}

model Category {
...

    @@schema("base")

}

model Course {
...

    instructor     User             @relation("CourseInstructor", fields: [userId], references: [id], onDelete: Cascade)
    modules        Module[]
    enrollments    Enrollment[]
    lessonProgress LessonProgress[]
    certificates   Certificate[]

    @@index([category])
    @@index([isPublished])
    @@index([averageRating]) // For sorting by rating
    @@map("courses")
    @@schema("base")

}

model Module {
...

    course  Course   @relation(fields: [courseId], references: [id], onDelete: Cascade)
    lessons Lesson[]

    @@map("modules")
    @@schema("base")

}

model Lesson {
...

    module   Module           @relation(fields: [moduleId], references: [id], onDelete: Cascade)
    progress LessonProgress[]

    @@map("lessons")
    @@schema("base")

}

model Enrollment {
...

    user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
    course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)

    @@unique([userId, courseId])
    @@index([userId])
    @@index([courseId])
    @@map("enrollments")
    @@schema("base")

}

model LessonProgress {
...

    user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
    lesson Lesson @relation(fields: [lessonId], references: [id], onDelete: Cascade)
    course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)

    @@unique([userId, lessonId])
    @@index([userId])
    @@map("lesson_progress")
    @@schema("base")

}

model Certificate {
...

    user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
    course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)

    @@map("certificates")
    @@schema("base")

}

model Event {
...

    host          User                @relation("EventHost", fields: [userId], references: [id], onDelete: Cascade)
    slots         EventSlot[]
    agenda        EventAgenda[]
    registrations EventRegistration[]

    @@index([startDate])
    @@index([averageRating]) // For sorting by rating
    @@map("events")
    @@schema("base")

}

model EventSlot {
...

    event Event @relation(fields: [eventId], references: [id], onDelete: Cascade)

    @@index([eventId])
    @@index([slotDate])
    @@map("event_slots")
    @@schema("base")

}

model EventAgenda {
...

    event Event @relation(fields: [eventId], references: [id], onDelete: Cascade)

    @@index([eventId])
    @@map("event_agenda")
    @@schema("base")

}

model EventRegistration {
...

    event Event @relation(fields: [eventId], references: [id], onDelete: Cascade)
    user  User? @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@map("event_registrations")
    @@schema("base")

}

model Post {
...

    author   User      @relation(fields: [userId], references: [id], onDelete: Cascade)
    comments Comment[]

    @@index([createdAt])
    @@index([averageRating]) // For sorting by rating
    @@index([userId])
    @@map("posts")
    @@schema("base")

}

model Comment {
...

    post    Post      @relation(fields: [postId], references: [id], onDelete: Cascade)
    author  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
    parent  Comment?  @relation("CommentReplies", fields: [parentId], references: [id], onDelete: Cascade)
    replies Comment[] @relation("CommentReplies")

    @@index([postId])
    @@index([userId])
    @@map("comments")
    @@schema("base")

}

model Like {
...

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@unique([userId, contentType, contentId, reactionType])
    @@index([userId])
    @@index([contentType])
    @@index([contentId])
    @@index([userId, contentType])
    @@index([contentType, contentId])
    @@index([createdAt])
    @@map("likes")
    @@schema("base")

}

model Rating {
...

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@unique([userId, contentType, contentId])
    @@index([userId])
    @@index([contentType])
    @@index([contentId])
    @@index([userId, contentType])
    @@index([contentType, contentId])
    @@index([rating])
    @@index([createdAt])
    @@index([contentType, contentId, rating]) // For filtering by rating value
    @@map("ratings")
    @@schema("base")

}

model Subscription {
...

    @@map("subscriptions")
    @@schema("base")

}

enum InvoiceStatus {
draft
issued
paid
partially_paid
canceled
fully_refunded

    @@schema("billing")

}

enum InvoiceType {
service
product
subscription

    @@schema("billing")

}

model Invoice {
...

    lines          InvoiceLine[]
    payments       Payment[]
    creditNotes    CreditNote[]
    zatcaDocuments ZatcaDocument[]

    @@map("invoices")
    @@schema("billing")

}

model InvoiceLine {
...

    invoice Invoice @relation(fields: [invoiceId], references: [id], onDelete: Cascade)

    @@index([invoiceId])
    @@map("invoice_lines")
    @@schema("billing")

}

enum PaymentProvider {
noon
tabby
stripe
manual

    @@schema("billing")

}

enum PaymentStatus {
pending
succeeded
failed

    @@schema("billing")

}

model Payment {
...

    invoice Invoice @relation(fields: [invoiceId], references: [id], onDelete: Cascade)

    @@index([invoiceId])
    @@schema("billing")

}

model CreditNote {
...

    invoice Invoice @relation(fields: [invoiceId], references: [id])

    createdAt      DateTime        @default(now()) @map("created_at") @db.Timestamptz
    updatedAt      DateTime        @default(now()) @updatedAt @map("updated_at") @db.Timestamptz
    zatcaDocuments ZatcaDocument[]

    @@map("credit_notes")
    @@schema("billing")

}

enum ZatcaDocumentType {
invoice
credit_note

    @@schema("billing")

}

enum ZatcaDocumentStatus {
pending_sign
signed
sign_failed
pending_report
reported
report_failed

    @@schema("billing")

}

model ZatcaDocument {
...

    invoice    Invoice?    @relation(fields: [invoiceId], references: [id])
    creditNote CreditNote? @relation(fields: [creditNoteId], references: [id])

    @@index([status, nextRetryAt])
    @@map("zatca_documents")
    @@schema("billing")

}

enum ZatcaEnvironment {
sandbox
production

    @@schema("billing")

}

model ZatcaSellerProfile {
...

    @@unique([environment])
    @@schema("billing")

}

model Affiliate {
...

    user        User              @relation(fields: [userId], references: [id], onDelete: Cascade)
    referrals   Referral[]
    commissions Commission[]
    payouts     AffiliatePayout[]

    @@index([status])
    @@index([referralCode])
    @@map("affiliates")
    @@schema("billing")

}

model Referral {
...

    affiliate    Affiliate    @relation(fields: [affiliateId], references: [id], onDelete: Cascade)
    referredUser User?        @relation(fields: [referredUserId], references: [id], onDelete: SetNull)
    commissions  Commission[]

    @@index([affiliateId])
    @@index([referredUserId])
    @@index([referralCode])
    @@index([status])
    @@map("referrals")
    @@schema("billing")

}

model Commission {
...

    affiliate Affiliate        @relation(fields: [affiliateId], references: [id], onDelete: Cascade)
    referral  Referral         @relation(fields: [referralId], references: [id], onDelete: Cascade)
    payout    AffiliatePayout? @relation(fields: [payoutId], references: [id], onDelete: SetNull)

    @@index([affiliateId])
    @@index([status])
    @@index([itemType])
    @@map("commissions")
    @@schema("billing")

}

model AffiliatePayout {
...

    affiliate   Affiliate    @relation(fields: [affiliateId], references: [id], onDelete: Cascade)
    commissions Commission[]

    @@index([affiliateId])
    @@index([status])
    @@map("affiliate_payouts")
    @@schema("billing")

}

model InvoiceSequence {
id Int @id @default(autoincrement()) @map("id")
invoiceType String @map("invoice_type") @db.VarChar(50)
year Int
currentValue Int @map("current_value")

    @@unique([id])
    @@index([invoiceType])
    @@index([year])
    @@index([currentValue])
    @@map("invoice_sequences")
    @@schema("seq")

}

model Share {
...

    user User? @relation(fields: [userId], references: [id], onDelete: SetNull)

    @@index([userId])
    @@index([contentType])
    @@index([contentId])
    @@index([platform])
    @@index([createdAt])
    @@map("shares")
    @@schema("base")

}

model Bookmark {
...

    user   User            @relation(fields: [userId], references: [id], onDelete: Cascade)
    folder BookmarkFolder? @relation(fields: [folderId], references: [id], onDelete: SetNull)

    @@unique([userId, contentType, contentId])
    @@index([userId])
    @@index([contentType])
    @@index([contentId])
    @@index([folderId])
    @@index([isPinned])
    @@index([createdAt])
    @@map("bookmarks")
    @@schema("base")

}

model BookmarkFolder {
...

    user      User             @relation(fields: [userId], references: [id], onDelete: Cascade)
    bookmarks Bookmark[]
    parent    BookmarkFolder?  @relation("BookmarkFolderHierarchy", fields: [parentId], references: [id], onDelete: Cascade)
    children  BookmarkFolder[] @relation("BookmarkFolderHierarchy")

    @@index([userId])
    @@index([parentId])
    @@index([sortOrder])
    @@map("bookmark_folders")
    @@schema("base")

}

model View {
...

    user User? @relation(fields: [userId], references: [id], onDelete: SetNull)

    // Unique constraint: logged-in users can only have one view per content
    @@unique([userId, contentType, contentId])
    // Index for anonymous tracking: IP + userAgent + contentType + contentId (handled in application logic)
    @@index([userId])
    @@index([contentType])
    @@index([contentId])
    @@index([ipAddress])
    @@index([sessionId])
    @@index([createdAt])
    @@index([contentType, contentId, createdAt]) // For analytics queries
    @@map("views")
    @@schema("base")

}

model Asset {
...

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([type])
    @@index([isPublic])
    @@index([createdAt])
    @@index([userId, type])
    @@map("assets")
    @@schema("base")

}

// ============================================================================
// Activity & Timeline
// ============================================================================

model Activity {
...

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([type])
    @@index([entityType, entityId])
    @@index([createdAt])
    @@index([userId, createdAt]) // For user timeline queries
    @@index([visibility, createdAt]) // For feed queries with visibility filtering
    @@map("activities")
    @@schema("base")

}

// ============================================================================
// Follow System
// ============================================================================

model Follow {
...

    follower  User @relation("UserFollowing", fields: [followerId], references: [id], onDelete: Cascade)
    following User @relation("UserFollowers", fields: [followingId], references: [id], onDelete: Cascade)

    @@unique([followerId, followingId]) // Prevent duplicate follows
    @@index([followerId])
    @@index([followingId])
    @@index([createdAt])
    @@map("follows")
    @@schema("base")

}

model Notification {
...

    user User @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([userId, isRead])
    @@index([userId, createdAt])
    @@index([type])
    @@index([entityType, entityId])
    @@index([isRead])
    @@map("notifications")
    @@schema("base")

}
