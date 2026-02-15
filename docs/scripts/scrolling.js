
function scrollToTop()
{
	window.scrollTo({ top: 0, behavior: 'smooth' });
}

function scrollToElement(elementID)
{
	let element = document.getElementById(elementID);
	window.scrollTo({ top: (element.offsetTop - 25), behavior: 'smooth' });
}
