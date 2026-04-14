
const fs = require('fs');
const path = require('path');

// Simulate the fetch logic
function testPath() {
    const mdFile = "./reprint/harness-engineering.md";
    const viewerDir = path.join(process.cwd(), 'docs');
    const absolutePath = path.resolve(viewerDir, mdFile);
    
    console.log("Viewer Dir:", viewerDir);
    console.log("MD File Path:", mdFile);
    console.log("Resolved Absolute Path:", absolutePath);
    
    if (fs.existsSync(absolutePath)) {
        console.log("[SUCCESS] File exists at expected location.");
    } else {
        console.log("[FAILURE] File NOT found at:", absolutePath);
    }
}

testPath();
