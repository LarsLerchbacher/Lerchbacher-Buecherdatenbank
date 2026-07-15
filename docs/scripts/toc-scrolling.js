// Add smooth scrolling to all table of contents links
document.addEventListener('DOMContentLoaded', function() {
    const tocLinks = document.querySelectorAll('a');
    tocLinks.forEach(link => {
        if (link.getAttribute('href')[0] == "#")
        {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                scrollToElement(targetId);
            });
        }   
    });
});
