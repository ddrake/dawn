function ajax_emailer_handler() {
  const links = document.getElementsByTagName("a");

  for (const link of links) {
    if (link.hasAttributes()) {
      for (const attr of link.attributes)
        if (attr.name = 'href' && attr.value.includes('send_user_instructions')) {
          link.addEventListener("click", function(e) {
	    const root = location.protocol + '//' + location.host;
            ajax_call(root + attr.value, e.target)
            e.preventDefault()
      	  })
        }
      }
    }
}

function ajax_call(url, element) {
  fetch(url, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    }
  })
  .then(response => {
    if (response.status != 200)
       alert(`Response status: ${response.status}`)
       return response.json()
  })
  .then(data => {
    console.log(data)
    if (data && data.result) {
      const td = element.parentElement.nextElementSibling;
      td.innerText = 'Y';
    }
    alert(data && data.result ? "The user was notified!" : "Notification failed!");
  });
}

window.addEventListener("load", (event) => {
  ajax_emailer_handler()
});

