# PowerShell脚本测试Google Gemini API
# 测试Google Gemini API的连接性

# 设置变量
$API_KEY = $env:GOOGLE_API_KEY
$MODEL = "gemini-2.5-flash-preview-05-20"
$IMAGE_PATH = "d:\codee\tableround\data\images\design_1749387656.png"

Write-Host "=== 测试Google Gemini API连接性 ===" -ForegroundColor Green

# 检查API密钥
if (-not $API_KEY) {
    Write-Host "❌ GOOGLE_API_KEY环境变量未设置" -ForegroundColor Red
    exit 1
}

Write-Host "✅ API Key: $($API_KEY.Substring(0, 10))..." -ForegroundColor Green

# 检查图片文件
if (-not (Test-Path $IMAGE_PATH)) {
    Write-Host "❌ 图片文件不存在: $IMAGE_PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 图片文件存在: $IMAGE_PATH" -ForegroundColor Green

# 将图片转换为Base64
Write-Host "🔄 转换图片为Base64..." -ForegroundColor Yellow
$imageBytes = [System.IO.File]::ReadAllBytes($IMAGE_PATH)
$base64Image = [System.Convert]::ToBase64String($imageBytes)

Write-Host "✅ Base64转换完成，长度: $($base64Image.Length)" -ForegroundColor Green

# 构建请求JSON字符串
$requestBody = @"
{
    "contents": [
        {
            "parts": [
                {
                    "text": "请详细描述这张图片的内容，包括颜色、形状、主题等。"
                },
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": "$base64Image"
                    }
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 1000
    }
}
"@

# 构建URL
$url = "https://generativelanguage.googleapis.com/v1beta/models/$MODEL`:generateContent?key=$API_KEY"

Write-Host "🔄 发送API请求..." -ForegroundColor Yellow
Write-Host "URL: $url" -ForegroundColor Cyan

try {
    # 发送请求
    $response = Invoke-RestMethod -Uri $url -Method POST -Body $requestBody -ContentType "application/json" -TimeoutSec 30
    
    Write-Host "✅ API请求成功!" -ForegroundColor Green
    
    # 解析响应
    if ($response.candidates -and $response.candidates[0].content.parts[0].text) {
        $result = $response.candidates[0].content.parts[0].text
        Write-Host "📝 响应内容:" -ForegroundColor Green
        Write-Host $result -ForegroundColor White
    } else {
        Write-Host "⚠️ 响应格式异常:" -ForegroundColor Yellow
        Write-Host ($response | ConvertTo-Json -Depth 5) -ForegroundColor White
    }
    
} catch {
    Write-Host "❌ API请求失败:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "HTTP状态码: $statusCode" -ForegroundColor Red
        
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorBody = $reader.ReadToEnd()
            Write-Host "错误详情: $errorBody" -ForegroundColor Red
        } catch {
            Write-Host "无法读取错误详情" -ForegroundColor Red
        }
    }
}

Write-Host "=== 测试完成 ===" -ForegroundColor Green
