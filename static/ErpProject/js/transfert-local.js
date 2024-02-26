transfertLocal = {};
/*
    Une ligne du transfert est un objet JSON de type :
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
transfertLocal.ajouterLigneTransfert = function (ligne) {
    ligne.type = "ligne-transfert";
    var data = JSON.stringify(ligne);
    localStorage.setItem(ligne.ligne_id, data);
};

/*
    Un ordre de transfert est un objet JSON de type :
    {
        numero,
        date_prevue,
        date_realisation,
        est_realisee,
        operation_stock_id,
        emplacement_origine_id,
        emplacement_destination_id,
        agent_id,
        reference_document,
        description
    }
*/
transfertLocal.ajouterTransfert = function (ordre) {
    var data = JSON.stringify(ordre);
    localStorage.setItem("transfert", data);
};

// Modifier la quantité d'une ligne de transfert
transfertLocal.modifierQuantite = function (ligne_id, quantite_demandee, quantite_fournie) {
    var data = localStorage.getItem(ligne_id);
    if(data != null && data != "" && ligne_id != "lsid")
    {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-transfert")
        {
            ligne.quantite_demandee = quantite_demandee;
            ligne.quantite_fournie = quantite_fournie;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

transfertLocal.supprimerLigne = function (ligne_id) {
    if(ligne_id != null && ligne_id != "" && ligne_id != "lsid") localStorage.removeItem(ligne_id);
};

transfertLocal.supprimerTransfert = function () {
    this.supprimerToutesLignes();
    localStorage.removeItem("transfert");
};

transfertLocal.supprimerToutesLignes = function () {
    var lignesTransfert = new Array();
    for (var i = 0; i < localStorage.length; i++)
    {
        var ligne_id = localStorage.key(i);
        if (ligne_id != "lsid" && ligne_id != "transfert" 
            && ligne_id != "commande" && ligne_id != "inventaire"
            && ligne_id != "transformation" && ligne_id != "fourniture"
            && ligne_id != "fabrication"
        )
        {
            var data = localStorage.getItem(ligne_id);
            var ligne = JSON.parse(data);
            if (ligne.type == "ligne-transfert") lignesTransfert.push(ligne);
        }
    }
    for(var i = 0; i < lignesTransfert.length; i++)
    {
        var ligne = lignesTransfert[i];
        localStorage.removeItem(ligne.ligne_id);
    }
};

transfertLocal.avoirToutesLignes = function () {
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
            if (ligne.type == "ligne-transfert") listeLignes.push(ligne);
        }
    }
    return listeLignes;
};

transfertLocal.avoirTransfert = function () {
    var transfert = null;
    var data = localStorage.getItem("transfert");
    if (data != null && data != "") transfert = JSON.parse(data);
    return transfert;
};

transfertLocal.refresh = function()
{
    localStorage.clear();
}