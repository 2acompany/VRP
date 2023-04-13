const BaseURL = () => {
    if(window.location.hostname == 'localhost') {
        return 'http://localhost:5000'
    }else{
      return 'https://vrp.shipito.ir'
    }
  }
  