fournitureLocal = {};
/*
    Une ligne de la fourniture est un objet JSON de type :
    {
        ligne_id,
        article_id,
        nom_article,
        stock_article_id,
        quantite_demandee,
        quantite_fournie,
        unite_achat_id,
        prix_unitaire,
        prix_lot,
        symbole_unite,
        type,
        description
    }
*/
fournitureLocal.ajouterLigneFourniture = function (ligne) {
    ligne.type = "ligne-fourniture";
    var data = JSON.stringify(ligne);
    localStorage.setItem(ligne.ligne_id, data);
};

/*
    Un ordre de fourniture est un objet JSON de type :
    {
        numero,
        date_prevue,
        date_realisation,
        est_realisee,
        devise_id,
        condition_reglement_id,
        fournisseur_id,
        receveur_id,
        reference_document,
        description
    }
*/
fournitureLocal.ajouterFourniture = function (ordre) {
    var data = JSON.stringify(ordre);
    localStorage.setItem("fourniture", data);
};

// Modifier la quantité d'une ligne de fourniture
fournitureLocal.modifierQuantite = function (ligne_id, quantite_demandee, quantite_fournie) {
    var data = localStorage.getItem(ligne_id);
    if(data != null && data != "" && ligne_id != "lsid")
    {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-fourniture")
        {
            ligne.quantite_demandee = quantite_demandee;
            ligne.quantite_fournie = quantite_fournie;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

fournitureLocal.modifierPrix = function (ligne_id, prix_unitaire, prix_lot) {
    var data = localStorage.getItem(ligne_id);
    if (data != null && data != "" && ligne_id != "lsid") {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-fourniture")
        {
            ligne.prix_unitaire = prix_unitaire;
            ligne.prix_lot = prix_lot;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

fournitureLocal.supprimerLigne = function (ligne_id) {
    if(ligne_id != null && ligne_id != "" && ligne_id != "lsid") localStorage.removeItem(ligne_id);
};

fournitureLocal.supprimerFourniture = function () {
    this.supprimerToutesLignes();
    localStorage.removeItem("fourniture");
};

fournitureLocal.supprimerToutesLignes = function () {
    var lignesFourniture = new Array();
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
            if (ligne.type == "ligne-fourniture") lignesFourniture.push(ligne);
        }
    }
    for(var i = 0; i < lignesFourniture.length; i++)
    {
        var ligne = lignesFourniture[i];
        localStorage.removeItem(ligne.ligne_id);
    }
};

fournitureLocal.avoirToutesLignes = function () {
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
            if (ligne.type == "ligne-fourniture") listeLignes.push(ligne);
        }
    }
    return listeLignes;
};

fournitureLocal.avoirFourniture = function () {
    var fourniture = null;
    var data = localStorage.getItem("fourniture");
    if (data != null && data != "") fourniture = JSON.parse(data);
    return fourniture;
};

fournitureLocal.refresh = function()
{
    localStorage.clear();
}