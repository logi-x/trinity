---
title: "Course Preview Example"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Preview Example

## Two Preview Modes Explained

The `CourseFormLayout` now supports two separate preview content slots, allowing you to optimize the user experience for both quick sidebar previews and full detailed modal previews.

## Why Two Separate Previews?

### Sidebar Preview (`previewContent`)

- **Limited space**: Only 400-480px wide
- **Always visible**: Updates in real-time as user types
- **Performance**: Should be lightweight and fast
- **Purpose**: Quick visual feedback during editing

### Modal Preview (`renderExpandedPreview`)

- **Full width**: Up to 1280px
- **On-demand**: Only rendered when user clicks Maximize
- **Performance**: Can be more complex/heavy
- **Purpose**: Final review before publishing

## Real-World Example

```tsx
import { CourseFormLayout } from "@experts/ui";
import { CompactCourseCard } from "./compact-course-card";
import { FullCourseView } from "./full-course-view";

export default function CreateCoursePage() {
  const [showPreview, setShowPreview] = useState(true);
  const { formData } = useCourseForm();

  return (
    <CourseFormLayout
      title="Create New Course"
      totalSteps={4}
      activeStep={1}
      stepTitles={["Information", "Details", "Curriculum", "Review"]}
      showPreview={showPreview}
      onTogglePreview={() => setShowPreview(!showPreview)}
      // Sidebar: Show compact card preview (400px wide)
      previewContent={
        <CompactCourseCard
          title={formData.title}
          description={formData.description}
          price={formData.price}
          thumbnail={formData.thumbnail}
          // Simplified - no modules/lessons
        />
      }
      // Modal: Show complete course page (1280px wide)
      renderExpandedPreview={() => (
        <FullCourseView
          title={formData.title}
          description={formData.description}
          price={formData.price}
          thumbnail={formData.thumbnail}
          modules={formData.modules} // Full curriculum
          instructor={formData.instructor} // Instructor bio
          reviews={formData.reviews} // Student reviews
          faqs={formData.faqs} // FAQ section
          // Complete production preview
        />
      )}
    >
      <CourseInformationForm />
    </CourseFormLayout>
  );
}
```

## Component Comparison

### Compact Preview (Sidebar)

```tsx
// compact-course-card.tsx
export function CompactCourseCard({ title, description, price, thumbnail }) {
  return (
    <Card>
      <CardBody>
        {/* Thumbnail */}
        <img src={thumbnail} className="aspect-video rounded-lg" />

        {/* Title */}
        <h3 className="mt-4 text-lg font-bold line-clamp-2">{title}</h3>

        {/* Description - truncated */}
        <p className="mt-2 text-sm text-gray-600 line-clamp-3">{description}</p>

        {/* Price */}
        <div className="mt-4 flex items-center justify-between">
          <span className="text-2xl font-bold">${price}</span>
          <Button size="sm" color="primary">
            Enroll
          </Button>
        </div>
      </CardBody>
    </Card>
  );
}
```

### Full Preview (Modal)

```tsx
// full-course-view.tsx
export function FullCourseView({
  title,
  description,
  price,
  thumbnail,
  modules,
  instructor,
  reviews,
  faqs,
}) {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="grid gap-8 lg:grid-cols-2">
        <div>
          <h1 className="text-4xl font-bold">{title}</h1>
          <p className="mt-4 text-lg text-gray-700">{description}</p>

          {/* Instructor */}
          <div className="mt-6 flex items-center gap-4">
            <Avatar src={instructor.avatar} size="lg" />
            <div>
              <p className="font-semibold">{instructor.name}</p>
              <p className="text-sm text-gray-600">{instructor.title}</p>
            </div>
          </div>
        </div>

        <div>
          <img src={thumbnail} className="rounded-xl shadow-lg" />

          {/* Enrollment Card */}
          <Card className="mt-4">
            <CardBody>
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold">${price}</span>
                <Button size="lg" color="primary">
                  Enroll Now
                </Button>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>

      {/* Course Curriculum */}
      <div>
        <h2 className="text-2xl font-bold">Course Curriculum</h2>
        <Accordion className="mt-4">
          {modules.map((module) => (
            <AccordionItem key={module.id} title={module.title}>
              <div className="space-y-2">
                {module.lessons.map((lesson) => (
                  <div key={lesson.id} className="flex items-center gap-2">
                    <PlayCircle className="h-4 w-4" />
                    <span>{lesson.title}</span>
                    <span className="ml-auto text-sm text-gray-500">
                      {lesson.duration}
                    </span>
                  </div>
                ))}
              </div>
            </AccordionItem>
          ))}
        </Accordion>
      </div>

      {/* Reviews */}
      <div>
        <h2 className="text-2xl font-bold">Student Reviews</h2>
        <div className="mt-4 space-y-4">
          {reviews.map((review) => (
            <Card key={review.id}>
              <CardBody>
                <div className="flex items-start gap-4">
                  <Avatar src={review.avatar} />
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <p className="font-semibold">{review.name}</p>
                      <div className="flex items-center gap-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={
                              i < review.rating ? "fill-yellow-400" : ""
                            }
                          />
                        ))}
                      </div>
                    </div>
                    <p className="mt-2 text-gray-600">{review.comment}</p>
                  </div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      </div>

      {/* FAQs */}
      <div>
        <h2 className="text-2xl font-bold">Frequently Asked Questions</h2>
        <Accordion className="mt-4">
          {faqs.map((faq) => (
            <AccordionItem key={faq.id} title={faq.question}>
              <p className="text-gray-700">{faq.answer}</p>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </div>
  );
}
```

## Benefits of Separate Previews

### Performance

- **Sidebar**: Lightweight, renders on every keystroke
- **Modal**: Heavy/complex, only renders when opened

### User Experience

- **Sidebar**: Quick visual feedback
- **Modal**: Complete picture before publishing

### Development

- **Sidebar**: Easy to maintain, simple component
- **Modal**: Can reuse actual production component

## Optional Modal

If you don't need a full preview modal, simply omit `renderExpandedPreview`:

```tsx
<CourseFormLayout
  // ... other props
  previewContent={<CompactPreview />}
  // No renderExpandedPreview - Maximize button won't appear
>
  <YourForm />
</CourseFormLayout>
```

## Best Practices

### Do's ✅

- Use `previewContent` for simplified, fast-updating preview
- Use `renderExpandedPreview` for complete, production-like preview
- Keep sidebar preview under 50 components
- Make modal preview match actual course page

### Don'ts ❌

- Don't put full course page in sidebar (too slow)
- Don't make sidebar preview too minimal (not useful)
- Don't forget to memoize modal preview if expensive
- Don't render modal content in sidebar (breaks layout)

## Example: E-commerce Course

```tsx
// Sidebar: Product card style
previewContent={
  <ProductCard
    image={formData.thumbnail}
    title={formData.title}
    price={formData.price}
    rating={4.5}
    students={1234}
  />
}

// Modal: Full product page
renderExpandedPreview={() => (
  <ProductPage
    hero={formData.hero}
    description={formData.description}
    curriculum={formData.modules}
    instructor={formData.instructor}
    testimonials={formData.reviews}
    pricing={formData.pricing}
    faqs={formData.faqs}
  />
)}
```

This separation ensures optimal performance and user experience at every stage of the course creation process.
