function scrollToTop()
{
	window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToElement(elementID)
{
	let element = document.getElementById(elementID);
	window.scrollTo({ top: (element.offsetTop - 25), behavior: 'smooth' });
}

window.onscroll = function() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("toTopButton").style.display = "block";
    } else {
        document.getElementById("toTopButton").style.display = "none";
    }
};
