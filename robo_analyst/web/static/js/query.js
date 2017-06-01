// const client = new ApiAi.ApiAiClient({accessToken: '537811f0da634c00b010543cc145a18e'});
// let promise = client.textRequest(longTextRequest);

// promise
//     .then(handleResponse)
//     .catch(heandleError);

// function handleResponse(serverResponse) {
//         console.log(serverResponse);
// }
// function heandleError(serverError) {
//         console.log(serverError);
// }

$(document).ready(function() {
    console.log('sanity check')


    var clientRequest = $('#client_request_panel');
    var convoData = $('#convo-data');
    var textResultField = $('#question-text-response');
    var textInput = $('input[name="query"]');
    var currentSession = null;



function queryApi(e) {
    e.preventDefault();
    console.log('in queryApi')

    
    var text = textInput.val();
    console.log(text);


    const client = new ApiAi.ApiAiClient({accessToken: '537811f0da634c00b010543cc145a18e', sessionId: currentSession});
    let promise = client.textRequest(text);


    promise
        .then(displayResults)
        .catch(heandleError);

    function handleResponse(response) {
            console.log(response);
    }
    function heandleError(serverError) {
            console.log(serverError);
    }

    function displayResults(response) {
        var result = response['result']
        currentSession = response['sessionId'];
        var speech = result['fulfillment']['speech'];
        var contexts = result['contexts'];
        var intent = result['metadata']['intentName'];

        var data = 'Intent: ' + intent;
        data += '<br></br>' + 'SessionId:' + currentSession;
        // data += '<br></br>' + JSON.stringify(result, undefined, 3);
        for (var i = 0; i < contexts.length; i++) {
            console.log(contexts[i])
            if (contexts[i]['name'] === 'data') {
                data += '<br></br>' + JSON.stringify(contexts[i]['parameters'], undefined, 3);
            } 
        }
        textInput.val('');
        textResultField.empty();
        convoData.empty();
        textResultField.append('<h4>' + speech + '</h4>');
        // convoData.append(JSON.stringify(data, undefined, 3));
        convoData.append(data);
        
    }
}




    
let queryForm = document.getElementById('query-form');
queryForm.addEventListener('submit', queryApi)
    
});