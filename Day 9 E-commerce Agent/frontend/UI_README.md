# AgenticCommerce AI - Frontend UI

## 🎨 Overview

This is the frontend interface for **AgenticCommerce AI**, a premium voice-powered e-commerce agent featuring a modern gradient design with indigo, purple, and pink colors.

## ✨ Features

### 🎭 Beautiful Design
- Modern gradient theme (Indigo → Purple → Pink)
- Glass-morphism effects
- Smooth animations
- Professional branding

### 🌓 Theme Support
- Light mode with soft pastels
- Dark mode with deep purples
- Automatic theme persistence
- Smooth transitions

### 📱 Responsive
- Mobile-first design
- Tablet optimized
- Desktop enhanced
- Touch-friendly

### ♿ Accessible
- WCAG AA compliant
- Keyboard navigation
- Screen reader friendly
- High contrast ratios

## 🚀 Quick Start

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── (app)/
│   │   ├── layout.tsx          # App layout wrapper
│   │   └── page.tsx            # Main page with tabs
│   ├── api/                    # API routes
│   ├── ui/                     # UI-specific routes
│   ├── layout.tsx              # Root layout
│   └── favicon.ico             # Favicon
│
├── components/
│   ├── app/
│   │   ├── app.tsx             # Main app component
│   │   ├── welcome-view.tsx    # Landing page
│   │   ├── session-view.tsx    # Active session view
│   │   └── ...                 # Other app components
│   ├── livekit/                # LiveKit UI components
│   └── ui/                     # Reusable UI components
│
├── styles/
│   └── globals.css             # Global styles & theme
│
├── public/
│   ├── commerce-logo.svg       # Custom logo
│   └── ...                     # Other assets
│
├── app-config.ts               # App configuration
└── package.json                # Dependencies
```

## 🎨 Design System

### Colors

```typescript
// Primary Colors
Indigo:  #6366f1
Purple:  #a855f7
Pink:    #ec4899

// Gradients
Primary: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)
```

### Typography

```typescript
// Font Families
Sans: Public Sans
Mono: Commit Mono

// Sizes
H1: 3rem (48px)
H2: 1.875rem (30px)
Body: 1rem (16px)
Small: 0.875rem (14px)
```

### Spacing

```typescript
// Padding Scale
Small:  1rem (16px)
Medium: 1.5rem (24px)
Large:  3rem (48px)

// Border Radius
Small:  0.75rem (12px)
Medium: 1rem (16px)
Large:  1.5rem (24px)
```

## 🎯 Key Components

### Welcome View
The landing page users see first:
- Animated background
- Hero section with branding
- Feature highlights
- Call-to-action button
- Example commands

**Location:** `components/app/welcome-view.tsx`

### Navigation Header
Top navigation with branding and tabs:
- Logo and tagline
- Three main tabs (Voice, Products, Orders)
- Gradient styling
- Icon integration

**Location:** `app/(app)/page.tsx`

### Theme Toggle
Bottom-center theme switcher:
- Light/dark mode toggle
- Smooth transitions
- Persistent preference

**Location:** `components/app/theme-toggle.tsx`

## 🎬 Animations

### Blob Animation
Floating background elements:
```css
Duration: 7s
Type: Infinite
Effect: Translate + Scale
```

### Hover Effects
Interactive element animations:
```css
Duration: 300ms
Effect: Scale(1.05) + Shadow
```

### Transitions
Smooth state changes:
```css
Duration: 300ms
Property: All
Timing: Ease-in-out
```

## 🛠️ Customization

### Change Branding

Edit `app-config.ts`:
```typescript
export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Your Company',
  pageTitle: 'Your Title',
  agentName: 'Your Agent',
  // ...
};
```

### Change Colors

Edit `styles/globals.css`:
```css
:root {
  --primary: #YOUR_COLOR;
  --accent: #YOUR_COLOR;
  --ring: #YOUR_COLOR;
}
```

### Change Welcome Message

Edit `components/app/welcome-view.tsx`:
```tsx
<h1>Your Custom Title</h1>
<p>Your custom description</p>
```

## 📦 Dependencies

### Core
- Next.js 14+
- React 18+
- TypeScript 5+

### UI
- Tailwind CSS 3+
- Radix UI
- Lucide Icons

### LiveKit
- @livekit/components-react
- livekit-client

## 🎯 Environment Variables

Create `.env.local`:
```bash
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
```

## 🧪 Testing

```bash
# Run tests
pnpm test

# Run linter
pnpm lint

# Type check
pnpm type-check
```

## 📱 Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome  | 90+     | ✅ Full |
| Firefox | 88+     | ✅ Full |
| Safari  | 14+     | ✅ Full |
| Edge    | 90+     | ✅ Full |

## 🎨 CSS Utilities

### Commerce-Specific

```css
.commerce-card
/* Glass-morphism card with purple border */

.commerce-badge
/* Gradient badge for labels */

.bg-gradient-commerce
/* Primary gradient background */

.card-hover
/* Hover effect with scale and shadow */
```

### Usage Example

```tsx
<div className="commerce-card card-hover p-6">
  <span className="commerce-badge">New</span>
  <h3>Product Name</h3>
</div>
```

## 🔧 Development Tips

### Hot Reload
Changes to components auto-reload in development mode.

### CSS Changes
Tailwind classes are JIT compiled - no restart needed.

### Type Safety
TypeScript provides full type checking across the app.

### Performance
- Use `next/image` for images
- Lazy load heavy components
- Optimize bundle size

## 📚 Documentation

- `COMMERCE_UI_GUIDE.md` - Complete design guide
- `UI_CHANGES_SUMMARY.md` - Change log
- `VISUAL_FEATURES.md` - Visual reference
- `QUICK_START_UI.md` - Quick start guide

## 🐛 Troubleshooting

### Styles Not Loading
```bash
rm -rf .next
pnpm dev
```

### Build Errors
```bash
pnpm clean
pnpm install
pnpm build
```

### Type Errors
```bash
pnpm type-check
```

## 🌟 Best Practices

1. **Use Semantic HTML** - Proper tags for accessibility
2. **Follow Tailwind Conventions** - Use utility classes
3. **Optimize Images** - Use WebP and proper sizes
4. **Test Responsiveness** - Check all breakpoints
5. **Maintain Consistency** - Follow design system

## 🎉 Features Showcase

### ✅ Implemented
- [x] Gradient theme
- [x] Glass-morphism
- [x] Animated backgrounds
- [x] Dark mode
- [x] Responsive design
- [x] Icon integration
- [x] Smooth transitions
- [x] Accessible components

### 🚀 Future Enhancements
- [ ] Product image gallery
- [ ] Advanced filters
- [ ] Wishlist feature
- [ ] User profiles
- [ ] Order tracking
- [ ] Reviews & ratings

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review console errors
3. Verify environment variables
4. Check browser compatibility

## 📄 License

This project is part of the AI Voice Agents Challenge by murf.ai

---

**AgenticCommerce AI** - Premium Voice Commerce Experience 🛍️✨

Built with Next.js, Tailwind CSS, and LiveKit
