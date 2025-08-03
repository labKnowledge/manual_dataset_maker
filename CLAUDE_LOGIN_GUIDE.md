# Claude Login Authentication Guide

This guide explains how to use Claude with login authentication instead of API keys.

## 🎯 Why Use Login Authentication?

### Advantages:
- **No API Key Required**: Use your regular Claude account
- **No Credit Card**: No need to add payment methods
- **Same Capabilities**: Access to all Claude features
- **Free Tier**: Use Claude's free tier limits

### Disadvantages:
- **Manual Setup**: Need to extract cookie from browser
- **Session Management**: Cookies expire and need refreshing
- **Rate Limits**: Subject to web interface rate limits
- **Less Stable**: Web interface can be less reliable than API

## 📋 Step-by-Step Cookie Extraction

### Method 1: Chrome/Edge Browser

1. **Login to Claude**
   - Go to https://claude.ai
   - Login with your account

2. **Open Developer Tools**
   - Press `F12` or right-click → "Inspect"
   - Go to "Application" tab

3. **Find Cookies**
   - In left sidebar, expand "Cookies"
   - Click on "https://claude.ai"

4. **Extract Session Key**
   - Find the cookie named `sessionKey`
   - Copy its value (it's a long string)

5. **Add to Environment**
   ```bash
   echo "CLAUDE_COOKIE=your_session_key_here" >> .env
   ```

### Method 2: Firefox Browser

1. **Login to Claude**
   - Go to https://claude.ai
   - Login with your account

2. **Open Developer Tools**
   - Press `F12` or right-click → "Inspect Element"
   - Go to "Storage" tab

3. **Find Cookies**
   - In left sidebar, expand "Cookies"
   - Click on "https://claude.ai"

4. **Extract Session Key**
   - Find the cookie named `sessionKey`
   - Copy its value

5. **Add to Environment**
   ```bash
   echo "CLAUDE_COOKIE=your_session_key_here" >> .env
   ```

### Method 3: Safari Browser

1. **Enable Developer Menu**
   - Safari → Preferences → Advanced
   - Check "Show Develop menu in menu bar"

2. **Login to Claude**
   - Go to https://claude.ai
   - Login with your account

3. **Open Developer Tools**
   - Develop → Show Web Inspector
   - Go to "Storage" tab

4. **Find Cookies**
   - In left sidebar, expand "Cookies"
   - Click on "https://claude.ai"

5. **Extract Session Key**
   - Find the cookie named `sessionKey`
   - Copy its value

## 🔧 Testing Your Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Login**
   ```bash
   python test_claude_login.py
   ```

3. **Run Main Script**
   ```bash
   python main_claude_login.py --dataset your_data.csv --character einstein
   ```

## ⚠️ Important Notes

### Cookie Security
- **Keep it Secret**: Don't share your cookie value
- **Don't Commit**: Never commit `.env` files to version control
- **Regular Refresh**: Cookies expire, refresh them periodically

### Rate Limits
- **Web Interface Limits**: Subject to Claude web interface rate limits
- **Slower Processing**: Web interface is slower than API
- **Connection Issues**: More prone to network issues

### Cookie Expiration
- **Automatic Expiry**: Cookies expire after some time
- **Session Timeout**: Inactive sessions timeout
- **Re-login Required**: You may need to re-login and get new cookie

## 🔄 Refreshing Your Cookie

When your cookie expires:

1. **Re-login to Claude**
   - Go to https://claude.ai
   - Login again if needed

2. **Extract New Cookie**
   - Follow the same extraction process
   - Get the new `sessionKey` value

3. **Update Environment**
   ```bash
   # Edit .env file and update CLAUDE_COOKIE
   nano .env
   ```

4. **Test Again**
   ```bash
   python test_claude_login.py
   ```

## 🚨 Troubleshooting

### Common Issues:

1. **"Invalid cookie" error**
   - Cookie has expired
   - Re-login and get new cookie

2. **"Connection failed" error**
   - Network connectivity issues
   - Claude service temporarily down

3. **"Rate limit exceeded" error**
   - Too many requests
   - Wait and try again later

4. **"Session expired" error**
   - Cookie has expired
   - Re-login and get new cookie

### Debug Mode:
```bash
# Run with verbose output
python test_claude_login.py --verbose
```

## 📊 Comparison: Login vs API Key

| Feature | Login Authentication | API Key |
|---------|-------------------|---------|
| **Setup** | Manual cookie extraction | Simple API key |
| **Cost** | Free tier | Pay per token |
| **Rate Limits** | Web interface limits | Higher limits |
| **Stability** | Less stable | More stable |
| **Features** | All web features | API features only |
| **Maintenance** | Cookie refresh needed | No maintenance |

## 🎯 Recommendation

**Use Login Authentication if:**
- You want to avoid API costs
- You're comfortable with manual setup
- You need all web interface features
- You're doing small to medium datasets

**Use API Key if:**
- You need high-volume processing
- You want maximum stability
- You're comfortable with costs
- You need programmatic reliability 