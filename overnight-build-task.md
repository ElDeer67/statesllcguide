# Overnight Build Task - StateBusinessGuide.com
**Execute at: 12:00 AM CST, February 27, 2026**
**Deadline: Ready for launch by 8:00 AM**

## Mission
Build ALL 50 state LLC pages for complete Friday launch. Site must be 100% ready for domain registration and Cloudflare deployment by 8 AM.

## Pages to Build (52 pages total)

### Step 1: Build Master Template (1 hour)
- Use CA/TX/FL as base
- Extract all common sections (90% of content)
- Create variables for state-specific data
- Template includes: steps, costs, timeline, FAQ, common mistakes, SEO tags

### Step 2: Compile State Data File (2-3 hours)
Research and document for all 50 states:
- Filing fee
- Annual report fee (if any)
- Processing time
- Entity name (LLC vs L.L.C. requirements)
- Publication requirements (NY, AZ only)
- Special quirks (franchise tax, etc.)

Save as: state-data.json

### Step 3: Generate All 50 Pages (1-2 hours)
Use template + state data to batch-generate:
- alabama-llc.html through wyoming-llc.html
- 2,500+ words each
- SEO optimized, mobile responsive
- Internal linking to homepage + other states

**Priority order (build these first):**
1. California (done)
2. Texas (done)
3. Florida (done)
4. New York
5. Illinois
6. Pennsylvania
7. Ohio
8. Georgia
9. North Carolina
10. Michigan
... through all 50

**Save progress every 10 pages** in case of timeout.

### Step 4: Homepage (index.html) (1 hour)
- **State selector:** Dropdown with all 50 states (alphabetical)
- **Quick comparison table:** Top 10 states by search volume
- **Value proposition:** "Complete LLC formation guides for all 50 states - Free, accurate, plain English"
- **Most popular guides:** Links to CA, TX, FL, NY, IL, PA, OH, GA, NC, MI (top 10)
- **Search volume stats:** Show combined 200K+ monthly searches
- Clean, fast, professional, mobile-first
- Internal linking to all 50 state pages

### 4. About Page
- Why trust us: Updated monthly, verified info, no upsells
- How we're different from LegalZoom/Incfile (we're free and honest)
- Commitment to accuracy
- Contact info (if needed later)
- Builds credibility for AdSense approval

## Technical Requirements

### All Pages Must Have:
- ✅ Proper meta tags (title, description, keywords)
- ✅ Mobile-responsive design
- ✅ Fast load time (<1 second)
- ✅ Internal linking (to other state pages + homepage)
- ✅ Footer with site navigation
- ✅ Consistent design matching CA/TX/FL
- ✅ Ad slot placeholders (5 per page)
- ✅ "Last updated: February 27, 2026" timestamp

### SEO Optimization:
- H1-H4 heading hierarchy
- Alt text for any images (if used)
- Schema markup (LocalBusiness/HowTo if applicable)
- Clean URL structure
- Internal linking strategy

### File Organization:
- Save all pages in: /Users/benrasche/.openclaw/workspace/state-business-guide/
- Update server.js to route all 7 pages
- Update index.html (homepage) with navigation to all pages

## Server Updates
- Update server.js to serve all 7 pages:
  - / → index.html (new homepage)
  - /california-llc.html
  - /texas-llc.html
  - /florida-llc.html
  - /new-york-llc.html (new)
  - /illinois-llc.html (new)
  - /about.html (new)

## Quality Checks
Before finishing, verify:
- [ ] All 7 pages load correctly
- [ ] All internal links work
- [ ] Mobile responsive (test viewport sizes)
- [ ] No broken links
- [ ] Consistent styling across all pages
- [ ] Ad placeholders in place
- [ ] SEO tags complete

## Deliverables
By 8:00 AM, have ready:
1. ✅ 50 state LLC pages (all states A-Z)
2. ✅ Homepage with 50-state navigation
3. ✅ About page
4. ✅ Updated server.js with routing for all 52 pages
5. ✅ Top 10 states tested and verified
6. ✅ Build summary report saved to: BUILD-REPORT-2026-02-27.md

**Minimum acceptable:** 30+ states completed if timeout occurs

## Success Criteria
- Ben wakes up to 50+ complete pages ready for launch
- Site launches with 200,000+ monthly search volume potential
- Instant authority as THE comprehensive LLC resource
- Complete site ready for Cloudflare deployment
- Domain can be registered (StateBusinessGuide.com)
- AdSense application can be submitted immediately
- Google Search Console submission ready
- Internal linking creates SEO compound effect from day one

---

**If anything fails or is unclear, document it in the build report and alert Ben via Telegram at 6 AM.**
