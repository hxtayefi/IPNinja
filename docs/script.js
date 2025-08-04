document.addEventListener('DOMContentLoaded', () => {
    // A central object for DOM elements
    const elements = {
        ipInput: document.getElementById('ipInput'),
        fileInput: document.getElementById('fileInput'),
        convertBtn: document.getElementById('convertBtn'),
        clearBtn: document.getElementById('clearBtn'),
        surgePolicy: document.getElementById('surgePolicy'),
        v2rayOutput: document.getElementById('v2rayOutput'),
        surgeOutput: document.getElementById('surgeOutput'),
        copyV2rayBtn: document.getElementById('copyV2rayBtn'),
        copySurgeBtn: document.getElementById('copySurgeBtn'),
        downloadV2rayBtn: document.getElementById('downloadV2rayBtn'),
        downloadSurgeBtn: document.getElementById('downloadSurgeBtn'),
        ipCountEl: document.getElementById('ipCount'),
        removeDuplicatesToggle: document.getElementById('removeDuplicatesToggle'),
        toastContainer: document.getElementById('toastContainer')
    };

    const utils = {
        /**
         * Parses text to get a clean list of valid IPs/CIDRs.
         * @param {string} text - The raw text from the textarea.
         * @returns {string[]} An array of cleaned IP strings.
         */
        getCleanIps: (text) => {
            const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\/(?:[0-9]|[12][0-9]|3[0-2]))?$/;
            return text.split('\n')
                .map(line => line.split('#')[0].trim()) // Remove comments and trim
                .filter(line => ipRegex.test(line));
        },
        
        /**
         * Displays a toast notification with an icon.
         * @param {string} message - The message to display.
         * @param {'info' | 'success' | 'error'} type - The type of toast.
         */
        showToast: (message, type = 'info') => {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            let icon;
            switch(type) {
                case 'success':
                    // Icon: Check Circle (Lucide)
                    icon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`;
                    break;
                case 'error':
                    // Icon: Alert Circle (Lucide)
                    icon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
                    break;
                default: // info
                    // Icon: Info (Lucide)
                    icon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
            }
            
            toast.innerHTML = `${icon}<span>${message}</span>`;
            elements.toastContainer.appendChild(toast);

            setTimeout(() => toast.classList.add('show'), 10);
            setTimeout(() => {
                toast.classList.remove('show');
                toast.addEventListener('transitionend', () => toast.remove());
            }, 3000);
        },
        
        /**
         * Triggers a file download.
         * @param {string} filename - The name of the file to download.
         * @param {string} content - The content of the file.
         */
        downloadFile: (filename, content) => {
            if (!content) {
                utils.showToast('Nothing to download.', 'error');
                return;
            }
            const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            utils.showToast(`Downloaded ${filename} successfully.`, 'success');
        },

        /**
         * Copies text from an element to the clipboard.
         * @param {HTMLTextAreaElement} outputElement - The element to copy text from.
         */
        copyToClipboard: (outputElement) => {
            const textToCopy = outputElement.value;
            if (!textToCopy) {
                utils.showToast('Nothing to copy.', 'error');
                return;
            }
            navigator.clipboard.writeText(textToCopy)
                .then(() => utils.showToast('Copied to clipboard!', 'success'))
                .catch(() => utils.showToast('Failed to copy.', 'error'));
        }
    };

    const handlers = {
        /** Updates the displayed IP count. */
        updateIpCount: () => {
            const ipCount = utils.getCleanIps(elements.ipInput.value).length;
            elements.ipCountEl.textContent = ipCount;
        },
        
        /** Handles the main conversion logic. */
        convert: () => {
            const rawIps = utils.getCleanIps(elements.ipInput.value);
            if (rawIps.length === 0) {
                utils.showToast('No valid IPs found to convert.', 'error');
                return;
            }

            const shouldRemoveDuplicates = elements.removeDuplicatesToggle.checked;
            const processedIps = shouldRemoveDuplicates ? [...new Set(rawIps)] : rawIps;
            
            const initialCount = rawIps.length;
            const finalCount = processedIps.length;
            const duplicatesRemoved = initialCount - finalCount;
            
            // Generate outputs
            elements.v2rayOutput.value = processedIps.join(',');
            elements.surgeOutput.value = processedIps.map(ip => `IP-CIDR,${ip},${elements.surgePolicy.value}`).join('\n');
            
            let toastMessage = `${finalCount} IP(s) converted successfully.`;
            if (shouldRemoveDuplicates && duplicatesRemoved > 0) {
                toastMessage += ` (${duplicatesRemoved} duplicates removed).`;
            }
            utils.showToast(toastMessage, 'success');
        },
        
        /** Clears all input and output fields. */
        clearAll: () => {
            elements.ipInput.value = '';
            elements.v2rayOutput.value = '';
            elements.surgeOutput.value = '';
            elements.fileInput.value = ''; // Reset file input
            handlers.updateIpCount();
            utils.showToast('Inputs and outputs cleared.', 'info');
        },

        /** Handles reading a .txt file. */
        handleFileUpload: (event) => {
            const file = event.target.files[0];
            if (file) {
                if (!file.name.endsWith('.txt')) {
                    utils.showToast('Please upload a valid .txt file.', 'error');
                    return;
                }
                const reader = new FileReader();
                reader.onload = (e) => {
                    elements.ipInput.value = e.target.result;
                    handlers.updateIpCount();
                    utils.showToast(`File "${file.name}" loaded successfully.`, 'success');
                };
                reader.readAsText(file);
            }
        }
    };

    // Attach all event listeners
    elements.ipInput.addEventListener('input', handlers.updateIpCount);
    elements.convertBtn.addEventListener('click', handlers.convert);
    elements.clearBtn.addEventListener('click', handlers.clearAll);
    elements.fileInput.addEventListener('change', handlers.handleFileUpload);
    elements.copyV2rayBtn.addEventListener('click', () => utils.copyToClipboard(elements.v2rayOutput));
    elements.copySurgeBtn.addEventListener('click', () => utils.copyToClipboard(elements.surgeOutput));
    elements.downloadV2rayBtn.addEventListener('click', () => utils.downloadFile('v2ray_rules.txt', elements.v2rayOutput.value));
    elements.downloadSurgeBtn.addEventListener('click', () => utils.downloadFile('surge_rules.conf', elements.surgeOutput.value));
    
    // Initial call to set the count
    handlers.updateIpCount();
});
