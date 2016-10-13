var NaturalLanguageClassifierV1 = require('watson-developer-cloud/natural-language-classifier/v1');

var natural_language_classifier = new NaturalLanguageClassifierV1({
    "password": "<password>",
    "username": "<username>"
});

var Converter = require("csvtojson").Converter;



var array = ["latercera", "Emol", "TVN", "CNNChile", "Cooperativa","eltreceoficial", "LANACION", "clarincom", "24conurbano", "populardiario","NoticiasRCN", "ELTIEMPO", "elespectador", "elpaiscali","CNNMex", "NTelevisa_com", "lopezdoriga", "EPN","abc_es", "informacion_es", "elperiodico", "_rebelion_org", "Overwatch_Esp", "radiocable","ElNuevoDia", "primerahora", "LaOpinionLA", "elnuevoherald", "vivelohoy", "despiertamerica"]



array.forEach(function(item) {
    var converter = new Converter({});
    console.log("big/" + item + "tweets.csv")

    converter.fromFile("big/" + item + "_tweets.csv", function(err, result) {
        if (!err) {
            //console.log(result)
            result.forEach(function(text) {

                natural_language_classifier.classify({
                    text: text.text,
                    classifier_id: text.class
                }, function(err, response) {
                    if (err)
                        console.log('error:', err);
                    else
                        console.log(JSON.stringify(response, null, 2));

               			console.log(result)
                });
            })
        }
    });
})
