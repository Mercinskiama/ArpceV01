fabricationLocal = {};
/*
    Une ligne de la fabrication est un objet JSON de type :
    {
        ligne_id,
        article_id,
        nom_article,
        stock_article_id,
        quantite_demandee,
        quantite_fournie,
        symbole_unite,
        type
    }
*/
fabricationLocal.ajouterLigneFabrication = function (ligne) {
    ligne.type = "ligne-fabrication";
    var data = JSON.stringify(ligne);
    localStorage.setItem(ligne.ligne_id, data);
};

/*
    Un ordre de fabrication est un objet JSON de type :
    {
        numero,
        date_prevue,
        date_realisation,
        est_realisee,
        article_id,
        quantite,
        agent_id,
        reference_document,
        description
    }
*/
fabricationLocal.ajouterFabrication = function (ordre) {
    var data = JSON.stringify(ordre);
    localStorage.setItem("fabrication", data);
};

// Modifier la quantité d'une ligne de fabrication
fabricationLocal.modifierQuantite = function (ligne_id, quantite_demandee, quantite_fournie) {
    var data = localStorage.getItem(ligne_id);
    if(data != null && data != "" && ligne_id != "lsid")
    {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-fabrication")
        {
            ligne.quantite_demandee = quantite_demandee;
            ligne.quantite_fournie = quantite_fournie;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

fabricationLocal.supprimerLigne = function (ligne_id) {
    if(ligne_id != null && ligne_id != "" && ligne_id != "lsid") localStorage.removeItem(ligne_id);
};

fabricationLocal.supprimerFabrication = function () {
    this.supprimerToutesLignes();
    localStorage.removeItem("fabrication");
};

fabricationLocal.supprimerToutesLignes = function () {
    var lignesFabrication = new Array();
    for (var i = 0; i < localStorage.length; i++)
    {
        var ligne_id = localStorage.key(i);
        if (ligne_id != "lsid" && ligne_id != "transfert" 
            && ligne_id != "commande" && ligne_id != "inventaire"
            && ligne_id != "transformation" && ligne_id != "fourniture"
            && ligne_id != "fabrication")
        {
            var data = localStorage.getItem(ligne_id);
            var ligne = JSON.parse(data);
            if (ligne.type == "ligne-fabrication") lignesFabrication.push(ligne);
        }
    }
    for(var i = 0; i < lignesFabrication.length; i++)
    {
        var ligne = lignesFabrication[i];
        localStorage.removeItem(ligne.ligne_id);
    }
};

fabricationLocal.avoirToutesLignes = function () {
    var nombreItems = localStorage.length;
    var listeLignes = new Array();
    for(var i = 0; i < nombreItems; i++)
    {
        var ligne_id = localStorage.key(i);
        if (ligne_id != "lsid" && ligne_id != "transfert" 
            && ligne_id != "commande" && ligne_id != "inventaire"
            && ligne_id != "transformation" && ligne_id != "fourniture"
            && ligne_id != "fabrication")
        {
            var data = localStorage.getItem(ligne_id);
            var ligne = JSON.parse(data);
            if (ligne.type == "ligne-fabrication") listeLignes.push(ligne);
        }
    }
    return listeLignes;
};

fabricationLocal.avoirFabrication = function () {
    var fabrication = null;
    var data = localStorage.getItem("fabrication");
    if (data != null && data != "") fabrication = JSON.parse(data);
    return fabrication;
};

fabricationLocal.refresh = function()
{
    localStorage.clear();
}