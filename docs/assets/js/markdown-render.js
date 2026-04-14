/**
 * Simple Markdown Renderer for Apple-style blog
 * Loads .md files and renders them into the .markdown-body container
 */

async function renderMarkdown() {
    const params = new URLSearchParams(window.location.search);
    let mdFile = params.get('file');
    const container = document.getElementById('markdown-container');

    if (!mdFile) {
        container.innerHTML = '<h1>未找到文件</h1><p>请在 URL 中提供有效的 <code>?file=...</code> 路径。</p>';
        return;
    }

    // Protocol Check (Help user avoid file:// issues)
    if (window.location.protocol === 'file:') {
        container.innerHTML = `
            <h1>无法在本地直接运行</h1>
            <p style="color: #ff3b30; font-weight: 600;">错误原因：浏览器由于安全限制，不允许在 <code>file://</code> 协议下进行 Fetch 请求。</p>
            <p><strong>解决方法：</strong></p>
            <ol style="text-align: left; display: inline-block; margin-top: 10px;">
                <li>在项目根目录运行本地服务器（如：<code>python -m http.server</code>）。</li>
                <li>访问 <code>http://localhost:8000/docs/index.html</code>。</li>
                <li>或者将代码推送至 GitHub Pages 自动部署。</li>
            </ol>
        `;
        return;
    }

    try {
        // Path Normalization
        mdFile = mdFile.trim();
        console.log('正在获取文件:', mdFile);
        
        const response = await fetch(mdFile);
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error(`文件未找到 (404)。请确认文件路径：${mdFile} 是否正确。`);
            }
            throw new Error(`HTTP 错误! 状态码: ${response.status}`);
        }
        
        const mdText = await response.text();
        console.log('文件获取成功，开始渲染...');

        // Verify if Marked library is available
        const markedInstance = window.marked?.marked || window.marked;
        if (typeof markedInstance === 'function' || (markedInstance && typeof markedInstance.parse === 'function')) {
            container.innerHTML = typeof markedInstance === 'function' ? markedInstance(mdText) : markedInstance.parse(mdText);
        } else {
            throw new Error('未检测到 Marked.js 渲染引擎。检查 CDN 链接是否被拦截？');
        }
        
        // Update document title from MD content
        const titleNode = container.querySelector('h1');
        if (titleNode) {
            document.title = titleNode.innerText + ' | 赵润泽的博客';
        }

    } catch (error) {
        console.error('渲染失败:', error);
        container.innerHTML = `
            <h1>加载失败</h1>
            <p style="color: #ff3b30;">${error.message}</p>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 14px; color: #666;">
                <strong>调试信息：</strong><br>
                请求文件: <code>${mdFile}</code><br>
                当前协议: <code>${window.location.protocol}</code><br>
                请确保文件存在于服务器的相应物理位置。
            </p>
        `;
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', renderMarkdown);
