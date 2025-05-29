// Cache elements first
const codeArea = document.querySelector('.code-area');
const lineNumbers = document.querySelector('.line-numbers');

function updateLineNumbers() {
    // Calculate number of lines
    const lineCount = codeArea.textContent.split('\n').length;
    
    // Generate line numbers
    lineNumbers.textContent = Array(lineCount).fill().map((_, i) => i + 1).join('\n');
    
    // Sync scroll positions
    lineNumbers.scrollTop = codeArea.scrollTop;
}

// Event Listeners
codeArea.addEventListener('input', updateLineNumbers);
codeArea.addEventListener('scroll', () => {
    lineNumbers.scrollTop = codeArea.scrollTop;
});

// Initial setup
updateLineNumbers();

// Handle Tab key
codeArea.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
        e.preventDefault();
        document.execCommand('insertText', false, '    ');
    }
});