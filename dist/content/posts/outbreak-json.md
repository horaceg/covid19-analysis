---
title: "Covid Outbreak - use json"
date: 2020-03-28T09:21:59+01:00
draft: true
---

<html>
<head>
  <style>
    .error {
        color: red;
    }
  </style>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4.0.2"></script>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>
</head>
<body>
  <div id="vis"></div>
  <script>
    function request() {
      let here = location.href;
      let thisUrl = here.substring(0, here.length - 15);
      let jsonUrl = thisUrl + 'combined.json';
      console.log(jsonUrl);
      // return fetch(jsonUrl).then(response => response.json())
      fetch(jsonUrl)
        .then((response) => {
          return response.json();
  })
    }
    async function request() {
      let here = location.href;
      let thisUrl = here.substring(0, here.length - 15);
      let jsonUrl = thisUrl + 'combined.json';
      console.log(jsonUrl);
      let data = await fetch(jsonUrl).then(response => response.json()) ;
      return data
    }

    (async function(vegaEmbed) {
      let data = await request();
      console.log(data);
      var spec = data;
      var embedOpt = {"mode": "vega-lite"};

      function showError(el, error){
          el.innerHTML = ('<div class="error" style="color:red;">'
                          + '<p>JavaScript Error: ' + error.message + '</p>'
                          + "<p>This usually means there's a typo in your chart specification. "
                          + "See the javascript console for the full traceback.</p>"
                          + '</div>');
          throw error;
      }
      const el = document.getElementById('vis');
      vegaEmbed("#vis", spec, embedOpt)
        .catch(error => showError(el, error));
    })(vegaEmbed);

  </script>
</body>
</html>