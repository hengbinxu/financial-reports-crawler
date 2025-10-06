from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# --- Nested Models for Ejerforhold (Ownership) ---


class ExtraDatalistItem(BaseModel):
    text_key: str | None = Field(default=None, alias="tekstnogle")
    value: str | None = Field(default=None, alias="vaerdi")
    value_text_key: str | None = Field(default=None, alias="vaerdiTekstnogle")


class ActiveLegalOwner(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    significant_influence_via_role: str | None = Field(
        default=None, alias="betydeligIndflydelseViaRolle"
    )
    significant_influence_via_role_list: list[Any] = Field(
        default_factory=list, alias="betydeligIndflydelseViaRollelist"
    )
    extra_data: str | None = Field(default=None, alias="ekstraData")
    extra_data_list: list[ExtraDatalistItem] = Field(
        default_factory=list, alias="ekstraDatalist"
    )
    unit_type: str | None = Field(default=None, alias="enhedstype")
    id: str | None = Field(default=None, alias="id")
    person_type: str | None = Field(default=None, alias="personType")
    latest_name: str | None = Field(default=None, alias="senesteNavn")
    sorting_value: int | None = Field(default=None, alias="sorteringsVaredi")
    title_prefix: Any | None = Field(default=None, alias="titlePrefix")


class Ownership(BaseModel):
    active_legal_owners: list[ActiveLegalOwner] = Field(
        default_factory=list, alias="aktiveLegaleEjere"
    )
    active_beneficial_owners: list[Any] = Field(
        default_factory=list, alias="aktiveReelleEjere"
    )
    beneficiary_group_name: str | None = Field(
        default=None, alias="begunstigetGruppeNavn"
    )
    beneficiary_group_legal_claim: str | None = Field(
        default=None, alias="begunstigetGruppeRetskrav"
    )
    board_considered_as_beneficial_owners: bool | None = Field(
        default=None, alias="bestyrelseAnsesSomReelleEjere"
    )
    owner_registration_under_five_percent: bool | None = Field(
        default=None, alias="ejerregistreringUnderFemProcent"
    )
    ceased_legal_owners: list[Any] = Field(
        default_factory=list, alias="ophoerteLegaleEjere"
    )
    ceased_beneficial_owners: list[Any] = Field(
        default_factory=list, alias="ophoerteReelleEjere"
    )
    company_unable_to_identify_beneficial_owners_management_installed: bool | None = (
        Field(
            default=None,
            alias="virksomhedHarIkkeKunnetIdentificereReelleEjereLedelseErIndsat",
        )
    )
    company_has_no_beneficial_owners_and_management_is_installed: bool | None = Field(
        default=None, alias="virksomhedHarIkkeReelleEjereOgLedelseErIndsat"
    )
    company_form_allows_beneficial_owner_information: bool | None = Field(
        default=None, alias="virksomhedsFormTilladerReelleEjerOplysninger"
    )


# --- Nested Models for HistoriskStamdata (HistoricalMasterData) ---


class HistoricalDataItem(BaseModel):
    valid_from: str | None = Field(default=None, alias="gyldigFra")
    valid_to: str | None = Field(default=None, alias="gyldigTil")
    value: str | None = Field(default=None, alias="vaerdi")


class HistoricalMasterData(BaseModel):
    address: list[Any] = Field(default_factory=list, alias="adresse")
    secondary_industry: list[Any] = Field(default_factory=list, alias="bibranche")
    industry_code: list[HistoricalDataItem] = Field(
        default_factory=list, alias="branchekode"
    )
    purpose: list[Any] = Field(default_factory=list, alias="formaal")
    name: list[HistoricalDataItem] = Field(default_factory=list, alias="navn")
    registered_capital: list[HistoricalDataItem] = Field(
        default_factory=list, alias="registreretKapital"
    )
    latest_articles_of_association_date: list[HistoricalDataItem] = Field(
        default_factory=list, alias="senesteVedtaegtsdato"
    )
    status: list[Any] = Field(default_factory=list, alias="status")
    signing_rule: list[Any] = Field(default_factory=list, alias="tegningsregel")
    foreign_address: list[Any] = Field(default_factory=list, alias="udenlandskAdresse")
    company_form: list[HistoricalDataItem] = Field(
        default_factory=list, alias="virksomhedsform"
    )


# --- Nested Models for Personkreds (CircleOfPersons) ---


class PersonRole(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    significant_influence_via_role: str | None = Field(
        default=None, alias="betydeligIndflydelseViaRolle"
    )
    significant_influence_via_role_list: Any | None = Field(
        default=None, alias="betydeligIndflydelseViaRollelist"
    )
    extra_data: str | None = Field(default=None, alias="ekstraData")
    extra_data_list: list[Any] = Field(default_factory=list, alias="ekstraDatalist")
    unit_type: str | None = Field(default=None, alias="enhedstype")
    id: str | None = Field(default=None, alias="id")
    person_type: str | None = Field(default=None, alias="personType")
    latest_name: str | None = Field(default=None, alias="senesteNavn")
    sorting_value: int | None = Field(default=None, alias="sorteringsVaredi")
    title_prefix: list[str] = Field(default_factory=list, alias="titlePrefix")


class Role(BaseModel):
    declaring_class: str | None = Field(default=None, alias="declaringClass")
    function_value: list[str] = Field(default_factory=list, alias="funktionsVaerdi")
    main_type: list[str] = Field(default_factory=list, alias="hovedType")
    sorting_value: int | None = Field(default=None, alias="sorteringsVaerdi")
    text_key: str | None = Field(default=None, alias="tekstnogle")


class CircleOfPersonsItem(BaseModel):
    person_roles: list[PersonRole] = Field(default_factory=list, alias="personRoller")
    role: Role | None = Field(default=None, alias="rolle")
    role_text_key: str | None = Field(default=None, alias="rolleTekstnogle")


class CircleOfPersons(BaseModel):
    owner_register_link: str | None = Field(default=None, alias="ejerborgLink")
    ceased_units: list[Any] = Field(default_factory=list, alias="ophoerteFad")
    circles_of_persons: list[CircleOfPersonsItem] = Field(
        default_factory=list, alias="personkredser"
    )
    signing_rule: str | None = Field(default=None, alias="tegningsregel")


# --- Nested Models for Produktionsenheder (ProductionUnits) ---


class AuditFirm(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    name: str | None = Field(default=None, alias="navn")
    p_number: str | None = Field(default=None, alias="pNummer")
    postal_code_and_city: str | None = Field(default=None, alias="postnummerOgBy")
    associated_auditors: Any | None = Field(default=None, alias="tilknyttedeRevisorer")


class MainIndustry(BaseModel):
    industry_code: str | None = Field(default=None, alias="branchekode")
    title: str | None = Field(default=None, alias="titel")


class ProductionUnitMasterData(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    secondary_industries: list[Any] = Field(default_factory=list, alias="bibrancher")
    building_number: Any | None = Field(default=None, alias="bygningsnummer")
    cvr_number: str | None = Field(default=None, alias="cvrnummer")
    email: str | None = Field(default=None, alias="email")
    open_on_holidays: bool | None = Field(default=None, alias="helligdagsaabent")
    main_industry: MainIndustry | None = Field(default=None, alias="hovedbranche")
    name: str | None = Field(default=None, alias="navn")
    cessation_date: Any | None = Field(default=None, alias="ophoersdato")
    p_number: str | None = Field(default=None, alias="pnummer")
    postal_code_and_city: str | None = Field(default=None, alias="postnummerOgBy")
    registered_in_money_laundering_register: bool | None = Field(
        default=None, alias="registreretIHvidvaskregistret"
    )
    financial_period_end: Any | None = Field(default=None, alias="regnskabsperiodeSlut")
    financial_period_start: Any | None = Field(
        default=None, alias="regnskabsperiodeStart"
    )
    advertising_protected: bool | None = Field(default=None, alias="reklamebeskyttet")
    start_date: str | None = Field(default=None, alias="startdato")
    telephone: Any | None = Field(default=None, alias="telefon")
    foreign_address: Any | None = Field(default=None, alias="udenlandskAdresse")
    foreign_address_country: str | None = Field(
        default=None, alias="udenlandskAdresseLand"
    )
    foreign_address_country_code: str | None = Field(
        default=None, alias="udenlandskAdresseLandekode"
    )
    company_name: Any | None = Field(default=None, alias="virksomhedsnavn")


class ActiveProductionUnit(BaseModel):
    number_of_employees: Any | None = Field(default=None, alias="antalAnsatte")
    historical_master_data: Any | None = Field(default=None, alias="historiskStamdata")
    audit_firm: AuditFirm | None = Field(default=None, alias="revisionsvirksomhed")
    master_data: ProductionUnitMasterData | None = Field(default=None, alias="stamdata")


class ProductionUnits(BaseModel):
    active_production_units: list[ActiveProductionUnit] = Field(
        default_factory=list, alias="aktiveProduktionsenheder"
    )
    ceased_production_units: list[Any] = Field(
        default_factory=list, alias="ophoerteProduktionsenheder"
    )


# --- Nested Models for SammenhaengendeRegnskaber (ConsecutiveFinancialStatements) ---


class DocumentReference(BaseModel):
    document_id: str | None = Field(default=None, alias="dokumentId")
    document_type: str | None = Field(default=None, alias="dokumenttype")
    content_type: str | None = Field(default=None, alias="indholdstype")


class FinancialStatement(BaseModel):
    reason_for_withdrawal: Any | None = Field(
        default=None, alias="begrundelseForTilbagetraekning"
    )
    cvr_number: str | None = Field(default=None, alias="cvrNummer")
    date_of_withdrawal: Any | None = Field(default=None, alias="datoForTilbageTrukket")
    chairman_name: str | None = Field(default=None, alias="dirigentNavn")
    document_type: str | None = Field(default=None, alias="dokumentType")
    document_references: list[DocumentReference] = Field(
        default_factory=list, alias="dokumentreferencer"
    )
    approval_date: str | None = Field(default=None, alias="godkendelsesdato")
    main_name: str | None = Field(default=None, alias="hovednavn")
    reporting_type: str | None = Field(default=None, alias="indberetningstype")
    publication_id: str | None = Field(default=None, alias="offentliggoerelseId")
    publication_timestamp: str | None = Field(
        default=None, alias="offentliggoerelseTidsstempel"
    )
    publication_timestamp_formatted: str | None = Field(
        default=None, alias="offentliggoerelseTidsstempelFormateret"
    )
    reversed: bool | None = Field(default=None, alias="omgjort")
    period_formatted: str | None = Field(default=None, alias="periodeFormateret")
    financial_period_from: str | None = Field(default=None, alias="regnskabsperiodeFra")
    financial_period_to: str | None = Field(default=None, alias="regnskabsperiodeTil")
    case_number: str | None = Field(default=None, alias="sagsnummer")
    withdrawn: bool | None = Field(default=None, alias="tilbagetrukket")


class ConsecutiveFinancialStatement(BaseModel):
    period_formatted: str | None = Field(default=None, alias="periodeFormateret")
    financial_statements: list[FinancialStatement] = Field(
        default_factory=list, alias="regnskaber"
    )
    financial_statement_type: str | None = Field(default=None, alias="regnskabsType")
    financial_period_from: str | None = Field(default=None, alias="regnskabsperiodeFra")
    financial_period_to: str | None = Field(default=None, alias="regnskabsperiodeTil")


# --- Nested Models for Stamdata (MasterData) ---


class MasterData(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    activities_covered_by_money_laundering_act: list[Any] = Field(
        default_factory=list, alias="aktiviteterOmfattetAfHvidvaskloven"
    )
    building_number: Any | None = Field(default=None, alias="bygningsnummer")
    cvr_number: str | None = Field(default=None, alias="cvrnummer")
    unit_number: str | None = Field(default=None, alias="enhedsnummer")
    has_pseudo_cvr: bool | None = Field(default=None, alias="harPseudoCvr")
    credit_information_code: Any | None = Field(
        default=None, alias="kreditoplysningskode"
    )
    parent_companies_in_case_of_franchise: list[Any] = Field(
        default_factory=list, alias="modervirksomhederVedFranchise"
    )
    name: str | None = Field(default=None, alias="navn")
    covered_by_money_laundering_act: bool | None = Field(
        default=None, alias="omfattetAfHvidvaskloven"
    )
    cessation_date: Any | None = Field(default=None, alias="ophoersdato")
    postal_code_and_city: str | None = Field(default=None, alias="postnummerOgBy")
    registration_number: Any | None = Field(default=None, alias="regnummer")
    advertising_protected: bool | None = Field(default=None, alias="reklamebeskyttet")
    social_economic_enterprise: bool | None = Field(
        default=None, alias="socialoekonomiskVirksomhed"
    )
    start_date: str | None = Field(default=None, alias="startdato")
    state_owned_enterprise: bool | None = Field(
        default=None, alias="statsligVirksomhed"
    )
    status: str | None = Field(default=None, alias="status")
    founded_before_1900_text_key: Any | None = Field(
        default=None, alias="stiftetFor1900Tekstnogle"
    )
    foreign_address: Any | None = Field(default=None, alias="udenlandskAdresse")
    foreign_address_country: str | None = Field(
        default=None, alias="udenlandskAdresseLand"
    )
    foreign_address_country_code: str | None = Field(
        default=None, alias="udenlandskAdresseLandekode"
    )
    effective_date: str | None = Field(default=None, alias="virkningsdato")
    company_form: str | None = Field(default=None, alias="virksomhedsform")
    company_form_code: str | None = Field(default=None, alias="virksomhedsformKode")
    show_name_postfix: bool | None = Field(default=None, alias="visNavnPostfix")


# --- Nested Models for UdvidedeOplysninger (ExtendedInformation) ---


class ExtendedInformation(BaseModel):
    secondary_industries: list[Any] = Field(default_factory=list, alias="bibrancher")
    secondary_names: list[Any] = Field(default_factory=list, alias="binavne")
    stock_exchange_listed: Any | None = Field(default=None, alias="boersnoteret")
    partially_paid_up_capital: bool | None = Field(
        default=None, alias="delvistIndbetaltKapital"
    )
    email: str | None = Field(default=None, alias="email")
    fax: Any | None = Field(default=None, alias="fax")
    first_financial_period_end: str | None = Field(
        default=None, alias="foersteRegnskabsperiodeSlut"
    )
    first_financial_period_start: str | None = Field(
        default=None, alias="foersteRegnskabsperiodeStart"
    )
    purpose: str | None = Field(default=None, alias="formaal")
    main_industry: MainIndustry | None = Field(default=None, alias="hovedbranche")
    capital_classes: bool | None = Field(default=None, alias="kapitalklasser")
    municipality: str | None = Field(default=None, alias="kommune")
    municipality_code: str | None = Field(default=None, alias="kommunekode")
    concession_date: Any | None = Field(default=None, alias="koncessionsdato")
    reorganization_period_end: Any | None = Field(
        default=None, alias="omlaegningsperiodeSlut"
    )
    reorganization_period_start: Any | None = Field(
        default=None, alias="omlaegningsperiodeStart"
    )
    postal_address: Any | None = Field(default=None, alias="postadresse")
    registered_capital: str | None = Field(default=None, alias="registreretKapital")
    financial_year_end: str | None = Field(default=None, alias="regnskabsaarSlut")
    financial_year_start: str | None = Field(default=None, alias="regnskabsaarStart")
    latest_articles_of_association_date: str | None = Field(
        default=None, alias="senesteVedtaegtsdato"
    )
    latest_articles_of_association_date_before_1900: bool | None = Field(
        default=None, alias="senesteVedtaegtsdatoFoer1900"
    )
    confirmation_date: Any | None = Field(default=None, alias="stadfaestelsesdato")
    confirmed_by: Any | None = Field(default=None, alias="stadfaestetAf")
    telephone: Any | None = Field(default=None, alias="telefon")
    secondary_telephone: Any | None = Field(default=None, alias="telefonSekundaert")
    foreign_postal_address: Any | None = Field(
        default=None, alias="udenlandskPostadresse"
    )
    foreign_postal_address_country: Any | None = Field(
        default=None, alias="udenlandskPostadresseLand"
    )
    foreign_postal_address_country_code: Any | None = Field(
        default=None, alias="udenlandskPostadresseLandekode"
    )


# --- Nested Models for VirksomhedRegistreringer (CompanyRegistrations) ---


class RegistrationText(BaseModel):
    text_with_link: str | None = Field(default=None, alias="tekstMedLink")
    text_without_link: str | None = Field(default=None, alias="tekstUdenLink")


class CompanyRegistration(BaseModel):
    address: str | None = Field(default=None, alias="adresse")
    cvr_number: str | None = Field(default=None, alias="cvrNummer")
    document_references: Any | None = Field(default=None, alias="dokumentReferencer")
    greenlandic_registration_number: Any | None = Field(
        default=None, alias="groenlandskRegistreringsnummer"
    )
    liberal_profession_registration_status: str | None = Field(
        default=None, alias="liberaleErhvervRegistreringsstatus"
    )
    name: str | None = Field(default=None, alias="navn")
    publication_id: str | None = Field(default=None, alias="offentliggoerelseId")
    publication_timestamp: str | None = Field(
        default=None, alias="offentliggoerelseTidsstempel"
    )
    heading: Any | None = Field(default=None, alias="overskrift")
    registration_text: RegistrationText | None = Field(
        default=None, alias="registreringsTekst"
    )
    registration_type: str | None = Field(default=None, alias="registreringstype")
    title_text_keys: list[str] = Field(default_factory=list, alias="titelTekstnogler")


# --- Main Response Model ---


class GetCompanyInfoByCvrNumberResponse(BaseModel):
    number_of_employees: dict[Any, Any] | None = Field(
        default=None, alias="antalAnsatte"
    )
    ownership: Ownership | None = Field(default=None, alias="ejerforhold")
    association_representatives: list[Any] = Field(
        default_factory=list, alias="foreningsrepraesentanter"
    )
    has_manual_signing: bool | None = Field(default=None, alias="harManuelSignering")
    historical_master_data: HistoricalMasterData | None = Field(
        default=None, alias="historiskStamdata"
    )
    parent_company: Any | None = Field(default=None, alias="hovedselskab")
    information_about_audit_firm: Any | None = Field(
        default=None, alias="oplysningerOmRevisionsvirksomhed"
    )
    circle_of_persons: CircleOfPersons | None = Field(default=None, alias="personkreds")
    production_units: ProductionUnits | None = Field(
        default=None, alias="produktionsenheder"
    )
    consecutive_financial_statements: list[ConsecutiveFinancialStatement] = Field(
        default_factory=list, alias="sammenhaengendeRegnskaber"
    )
    hide_other_documents: bool | None = Field(
        default=None, alias="skjulOevrigeDokumenter"
    )
    master_data: MasterData | None = Field(default=None, alias="stamdata")
    extended_information: ExtendedInformation | None = Field(
        default=None, alias="udvidedeOplysninger"
    )
    company_registrations: list[CompanyRegistration] = Field(
        default_factory=list, alias="virksomhedRegistreringer"
    )
    company_announcements: list[Any] = Field(
        default_factory=list, alias="virksomhedsMeddelelser"
    )
