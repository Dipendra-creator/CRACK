# Testing Guide - Leakosint Telegram Bot

## Quick Test Checklist

### ✅ Pre-Testing Setup

1. **Check Environment Variables**
   ```bash
   # Ensure .env file has:
   LEAKOSINT_API_URL=https://leakosintapi.com/
   LEAKOSINT_API_TOKEN=your_token_here
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

2. **Install Dependencies**
   ```bash
   pip install python-dotenv requests pyTelegramBotAPI
   ```

3. **Verify Bot Code**
   ```bash
   python -m py_compile main.py
   ```

### 🧪 Test Scenarios

#### Test 1: Basic Search
**Input:** `918433220261`

**Expected Output:**
- Metadata displayed (NumOfDatabase, NumOfResults, etc.)
- Database name(s) shown with 📊 icon
- InfoLeak information displayed
- All records numbered (Record #1, Record #2, etc.)
- All fields in each record displayed
- Navigation buttons (if multiple pages)

#### Test 2: Email Search
**Input:** `test@example.com`

**Expected Output:**
- Same structure as Test 1
- All email-related fields shown
- Any associated data displayed

#### Test 3: No Results
**Input:** `nonexistent_query_12345`

**Expected Output:**
- Error message or "No results found"
- Metadata still shown if available

#### Test 4: API Error
**Simulate:** Invalid API token

**Expected Output:**
- Clear error message
- Suggestion to check configuration

### 📋 Field Display Verification

Ensure ALL these fields are displayed when present:

**Metadata Fields:**
- ✅ NumOfDatabase
- ✅ NumOfResults
- ✅ free_requests_left
- ✅ price
- ✅ search time

**Database Fields:**
- ✅ InfoLeak
- ✅ NumOfResults (per database)
- ✅ Data (all records)

**Record Fields (from sample data):**
- ✅ Address, Address2, Address3
- ✅ DocNumber
- ✅ FatherName
- ✅ FullName
- ✅ Phone, Phone2, Phone3
- ✅ Region
- ✅ Email (if present)
- ✅ Age, Gender, District, State (ICMR data)
- ✅ **ANY NEW FIELDS** (this is the key test!)

### 🔍 Generic Handling Tests

#### Test A: New Field Added
**Scenario:** API adds a new field "NewField"

**Expected:** Field automatically displayed without code changes

#### Test B: Nested Data
**Scenario:** API returns nested objects/arrays

**Expected:** Properly indented recursive display

#### Test C: Different Data Types
**Scenario:** Fields with strings, numbers, booleans, nulls

**Expected:** All types displayed correctly

### 🎯 Navigation Tests

1. **Single Page Result**
   - No navigation buttons shown

2. **Multiple Page Result**
   - Previous/Next buttons shown
   - Page counter displays (e.g., "1/3")
   - Clicking Next shows next page
   - Clicking Previous shows previous page
   - Wrapping works (last page → first page)

### 🚀 Running the Bot

```bash
# Start the bot
python main.py

# You should see:
# INFO - Starting Leakosint Telegram Bot...
# INFO - Bot configured with API token: 1799933101...
# INFO - Bot is running and waiting for messages...
```

### 📱 Telegram Testing

1. **Start Command**
   ```
   /start
   ```
   Expected: Welcome message with menu buttons

2. **Help Command**
   ```
   /help
   ```
   Expected: Complete help guide

3. **Stats Command**
   ```
   /stats
   ```
   Expected: Bot statistics with current cache count

4. **Examples Command**
   ```
   /examples
   ```
   Expected: Search examples for different query types

5. **Search Query**
   ```
   918433220261
   ```
   Expected: Full search results with all data

### 🐛 Debugging

**If data is missing:**
1. Check logs for API response
2. Verify `format_value()` is being called
3. Check if field is in excluded list (should only be InfoLeak, NumOfResults, Data)

**If formatting is wrong:**
1. Check indentation levels
2. Verify recursive calls are working
3. Test with `test_formatting.py`

**If bot crashes:**
1. Check error logs
2. Verify API token is valid
3. Check network connectivity

### 📊 Sample Test Output

```
📊 Search Results

NumOfDatabase: 2
NumOfResults: 5
free_requests_left: 50
price: 0
search time: 0.0155468

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 HiTeckGroop.in

ℹ️ Info: At the beginning of 2025, a huge leak...

📈 Results: 3

━━━ Record #1 ━━━
• Address: W/O Rakesh Kumar,77rampurgabhana...
• Address2: W/O Rakesh Kumar,77,rampur...
• Address3: W/O Rakesh Kumar,rampur...
• DocNumber: 672811474313
• FatherName: Omwati
• FullName: Rakesh Kumar
• Phone: 918433220261
• Phone2: 918171994779
• Phone3: 917060249537
• Region: AIRTEL UPW;Airtel UP West;JIO UPW

[... more records ...]
```

### ✅ Success Criteria

- [ ] All metadata fields displayed
- [ ] All database names shown
- [ ] InfoLeak information visible
- [ ] All records numbered correctly
- [ ] **Every field in every record is displayed**
- [ ] Nested data properly formatted
- [ ] Navigation works smoothly
- [ ] No crashes or errors
- [ ] Clean, readable output
- [ ] HTML formatting works (bold text, icons)

### 🎉 Final Verification

Run the test script:
```bash
python test_formatting.py
```

Expected output: Complete data display with all fields from sample response.

---

## Notes

- The bot is now **completely generic** - it will display ANY field from the API
- No code changes needed when API structure changes
- All data is preserved and displayed
- Format is clean and user-friendly
