categorical_phrases = dict()
categorical_pairs = dict()

def add_case_variations(phrases):
    """
    Adds both capitalized and lowercase versions of the given phrases.
    """
    new_phrases = set()

    for phrase in phrases:
        # Add both capitalized and lowercase versions of the phrase
        new_phrases.add(phrase.lower())
        new_phrases.add(phrase.capitalize())  # Capitalize the first letter
        
    return new_phrases

def update_pairs_with_case_variations(pairs):
    """
    Updates the pairs dictionary to include both capitalized and lowercase versions of the phrases and subcategories.
    """
    updated_pairs = {}
    
    for category, pair_dict in pairs.items():
        updated_pair_dict = {}
        
        for subcategory, phrases in pair_dict.items():
            # Add case variations for subcategories as well
            updated_subcategory_variations = add_case_variations([subcategory])
            updated_pair_dict.update({sub: add_case_variations(phrases) for sub in updated_subcategory_variations})
        
        updated_pairs[category] = updated_pair_dict
    
    return updated_pairs

## Fact
categorical_phrases['F'] = [
	'appellant', 'dated', 'No.', 'State', 'filed', 'Government', 'registration', 'basis', 'stated', 'notice', 'period', 
	'region', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
	'the plaintiff', 'the basis', 'basis of', 'Court of', 'stated that', 'filed a', 'was issued', 'the Constitution', 
	'the Corporation', 'under Article', 'plaintiff and', 'show cause', 'High court of', 'that the said', 'referred to as', 
	'stated that the', 'In the year',
	'commenced', 'allegations', 'submitted', 'documentation', 'presented', 'filed suit', 'action initiated', 'notice of motion',
	'listed', 'parties involved', 'first instance', 'complaint lodged', 'hearing date', 'initial complaint', 'plaintiff asserted',
	'factual matrix', 'chronology of events', 'occurrence of', 'evidence produced', 'supporting documents', 'background of the case',
	'arising out of', 'submitted evidence', 'recorded statements', 'under consideration', 'incident occurred', 'in relation to',
	'examination of facts', 'witness testimony', 'facts of the case', 'event leading to', 'material facts', 'factual background',
	'established that', 'proven by', 'nature of complaint', 'resulting in', 'case initiated', 'process initiated', 'led to', 
	'submission of evidence', 'following incident', 'on the basis of', 'material presented', 'according to records', 'initial findings',
	'presented before court', 'facts provided', 'investigation report', 'cause of action', 'factual determination', 'led to litigation',
	'dispute arising from', 'events surrounding', 'circumstances of', 'pertinent facts', 'filing of case', 'case number', 'legal proceedings',
	'documentation provided', 'incidents described', 'filed under', 'complaint filed', 'case details', 'factual circumstances',
	'procedural background', 'litigation details', 'registered under', 'outlined facts', 'factual submissions', 'statement of facts',
	'actions undertaken', 'legal action taken', 'relevant facts', 'documented proceedings', 'initiating legal process', 'prior to filing',
	'criminal action', 'civil suit', 'incident leading to', 'legal cause', 'lawsuit commenced', 'official report', 'records of case',
	'factual claim', 'entered into evidence', 'cause leading to', 'related documentation', 'basis for litigation', 'circumstances described',
	'presented argument', 'trial proceedings', 'materials submitted', 'factual basis', 'allegations made', 'claim submitted',
	'details outlined', 'sequence of events', 'cause of dispute', 'raised issue', 'description of events', 'matter referred',
	'initial allegations', 'filed at court', 'grounds for filing', 'litigation commenced', 'written complaint', 'preceding events',
	'chronological sequence'
]

categorical_pairs['F'] = {
    'Plaintiff': ['filed the case', 'initiated proceedings', 'alleges that', 'has approached the court', 'claimed damages from', 'instituted the suit', 'contested the issue', 'brought forward the claim', 'pleaded for relief', 'has sought redressal', 'is the aggrieved party', 'seeks compensation for', 'contended against', 'asserted the right to', 'opposed the defense'],
    'Appellant': ['has filed an appeal', 'contends the decision', 'appeals the order', 'has questioned the ruling', 'moved for revision of the judgment', 'challenged the conviction', 'filed an appeal before', 'appealed against the order', 'has objected to', 'pleaded for the setting aside of the judgment', 'opposes the sentence passed', 'claims the right to appeal', 'seeks appellate relief', 'has filed for a reconsideration'],
    'Notice': ['was issued to', 'of termination', 'of eviction', 'of intent', 'served upon', 'of demand', 'of assessment', 'of default', 'of deficiency', 'was served on the plaintiff', 'given to the defendant', 'was duly served', 'of compensation', 'issued by the authority', 'of seizure', 'issued under the provisions', 'to vacate', 'was received by the party', 'was signed by', 'of hearing'],
    'Period': ['of limitation', 'of lease', 'of tenancy', 'for appeal', 'of repayment', 'of contract', 'for filing objections', 'of employment', 'for completion', 'for hearing', 'of deferment', 'of notice'],
    'State': ['of affairs', 'Government of', 'under jurisdiction', 'in the territory of', 'subject to the laws of', 'responsibility of', 'administered by', 'controlled by the authority', 'within the borders of', 'mandated by', 'granted by', 'within the state of', 'covered by', 'recognized by', 'regulated by', 'the subject of', 'in the territory of', 'subject to the policies of'],
    'Dated': ['on this day', 'signed on', 'issued on', 'of service', 'of transaction', 'of filing', 'on the date mentioned', 'on or around', 'for the date of', 'indicated in the contract', 'on the complaint of', 'for the purposes of', 'was effective from', 'on the representation of', 'filed on', 'was decided on'],
    'Registration': ['certificate issued', 'granted to', 'under Act', 'under the provisions of', 'in the name of', 'is confirmed', 'was cancelled', 'was required for', 'was transferred to', 'was authorized under', 'was completed by', 'was renewed on', 'was updated by', 'was recorded as', 'was not received by', 'was rejected by', 'is pending for', 'was lodged with the', 'was accepted by'],
    'Court': ['of law', 'has jurisdiction', 'proceeds with the case', 'held that', 'granted permission to', 'issued an order', 'decided in favor of', 'rejected the claim of', 'accepted the argument of', 'allowed the appeal', 'stayed the proceedings', 'heard the petition of', 'deferred the decision', 'dismissed the complaint', 'set aside the ruling', 'remanded the case', 'granted an extension for'],
    'Filed': ['a petition', 'an application', 'a complaint', 'an affidavit', 'a motion', 'a counterclaim', 'a writ', 'for damages', 'for compensation', 'for annulment', 'for review', 'for an injunction', 'for an appeal', 'for reconsideration', 'for an extension', 'for permission', 'for stay', 'for reinstatement', 'for discharge'],
    'Case': ['involving the plaintiff', 'against the defendant', 'pertaining to the contract', 'under consideration', 'was brought forward', 'is currently pending', 'was decided upon', 'was dismissed', 'was set aside', 'was reopened by the court'],
    'Agreement': ['was signed between', 'was breached by', 'was upheld by the court', 'was terminated by', 'was enforced under', 'was disputed by', 'was executed on', 'was declared void'],
    'Contract': ['was entered into', 'was violated by', 'was honored by', 'was terminated by', 'was breached by', 'stipulated the terms of', 'granted the rights to', 'was in dispute', 'was extended by mutual consent', 'was subject to renewal'],
    'Property': ['was owned by', 'was transferred to', 'was sold by', 'was registered in the name of', 'was held by', 'is located in', 'is subject to mortgage', 'is in dispute', 'was leased to'],
    'Claim': ['for compensation', 'for damages', 'for reinstatement', 'was lodged by', 'was denied by', 'was upheld by the court', 'was rejected by', 'was dismissed', 'was pursued by', 'for reimbursement'],
    'Document': ['was submitted to', 'was filed with', 'was signed by', 'was drafted by', 'was executed on', 'was declared invalid', 'was recognized by', 'was acknowledged by', 'was issued under'],
}

## Issue
categorical_phrases['I'] = [
	'appeal by', 
	'question of law', 'legal issue', 'dispute over', 'subject to', 'controversy concerning', 'matter raised', 'contention arose',
	'point of dispute', 'matter under consideration', 'subject matter of', 'central issue', 'disputed fact', 'conflicting opinions',
	'legal standing', 'procedural issue', 'point of law', 'key issue', 'contested matter', 'legal interpretation', 'matter in question',
	'issue of fact', 'matter for adjudication', 'question of jurisdiction', 'primary issue', 'conflict of interest', 'question of authority',
	'legality of action', 'dispute between parties', 'inconsistency in facts', 'issue of interpretation', 'primary question', 'debated issue',
	'concern over', 'point of contention', 'interpretative issue', 'matter for determination', 'legal question', 'dispute over terms',
	'conflicting claims', 'problem raised', 'interpretation of statute', 'validity of claim', 'procedural question', 'substantive issue',
	'judicial question', 'question raised by', 'legal definition', 'issue before court', 'key legal matter', 'fundamental issue',
	'procedural irregularity', 'core dispute', 'disagreement over facts', 'jurisdictional question', 'nature of dispute', 'ambiguity in law',
	'conflicting statutes', 'rights contested', 'legal challenge', 'issue of legality', 'legal complication', 'dispute regarding',
	'jurisdictional dispute', 'question of rights', 'challenge to authority', 'query raised', 'main issue', 'contested right', 'principle in dispute',
	'cause of contention', 'dispute around', 'rights involved', 'constitutional issue', 'infringement of rights', 'matter of law', 'issue on appeal',
	'fundamental disagreement', 'question over', 'question of constitutionality', 'rights at issue', 'legal conflict', 'procedural conflict',
	'matter of dispute', 'main contention', 'legal question presented', 'point of concern', 'question of interpretation', 'core legal question',
	'primary legal issue', 'factual disagreement', 'contested interpretation', 'query about', 'subject matter of dispute', 'disagreement over interpretation',
	'dispute in case', 'legal point', 'jurisdictional issue', 'issue of responsibility', 'legal dispute raised', 'contention in court',
	'legal dispute at hand'
]

categorical_pairs['I'] = {
    'Appeal': ['filed by', 'was dismissed', 'was allowed', 'was upheld by', 'was rejected by', 'is pending before', 'was challenged by', 'was heard by', 'was reversed by', 'was remitted by', 'was argued in court', 'was subject to review'],
    'Court': ['of appeal', 'has jurisdiction over', 'considers the case', 'granted an injunction', 'held that', 'rejected the plea of', 'issued notice to', 'granted an extension for', 'dismissed the complaint', 'heard the arguments of', 'granted relief to', 'stayed the proceedings'],
    'Judgment': ['was rendered by', 'was appealed against', 'was upheld in', 'was passed in favor of', 'was challenged by', 'was quashed by', 'was stayed by', 'was set aside by', 'was referred back to', 'was delivered ex-parte', 'was declared void', 'was recorded on'],
    'Matter': ['of concern', 'under dispute', 'under consideration', 'of law', 'of fact', 'arising from', 'relating to', 'of contract', 'of equity', 'of rights', 'in controversy', 'pertaining to', 'of property', 'pending in court', 'for adjudication', 'to be resolved'],
    'Dispute': ['over ownership', 'regarding rights', 'on breach of contract', 'on payment terms', 'between the parties', 'arising from the agreement', 'on intellectual property', 'on tenancy rights', 'on patent infringement', 'concerning liability', 'over compensation', 'relating to performance', 'regarding employment', 'on partnership issues', 'on boundary rights', 'on service agreement'],
    'Controversy': ['arose in', 'was between the parties', 'was settled by', 'was unresolved', 'was referred to arbitration', 'surrounded the question of', 'was based on', 'was resolved by the court', 'involved a question of law', 'was subject to judicial review', 'was negotiated between', 'centered on the issue of'],
    'Claim': ['of damages', 'for compensation', 'for reinstatement', 'was dismissed by the court', 'was allowed by the court', 'was settled out of court', 'was disputed by', 'was defended by', 'was filed in relation to', 'for reimbursement', 'for relief from', 'for specific performance'],
    'Legal': ['grounds for appeal', 'issues raised', 'question involved', 'rights protected by', 'obligations under', 'liability imposed by', 'responsibility determined by', 'provisions applicable to', 'remedies available under', 'actions authorized by'],
    'Section': ['of the Act', 'under which the case falls', 'that applies in this case', 'was referred to in the judgment', 'was cited by the counsel', 'was invoked by the plaintiff', 'provides for', 'grants the right to', 'restricts the authority of', 'governs the procedures of'],
    'Relief': ['sought by the plaintiff', 'granted by the court', 'was denied to the appellant', 'was awarded to the respondent', 'was allowed by the tribunal', 'was refused by the court', 'was requested in the petition', 'was subject to conditions', 'was rejected in the application'],
}

## Argument
categorical_phrases['A'] = [
	'service', 'amount', 'value', 'section', 'goods', 'credit', 'license', 'supplied', 'recipient', 'country', 'quota', 'contended', 
	'contention', 'under Section', 'terms of', 'counsel for', 'before us', 'charged by', 'is charged', 'free of', 'charged by the', 'provided by the',
	'pleaded', 'submitted that', 'maintained that', 'argued before', 'contention raised', 'alleged that', 'asserted that', 'emphasized',
	'rebuttal by', 'insisted that', 'claimed that', 'sought to prove', 'established through', 'defense argued', 'put forward', 'raised objection',
	'challenged by', 'responded to', 'contested claim', 'presented defense', 'denied by', 'submitted evidence', 'raised concern', 'raised objection',
	'contentions of parties', 'argued on behalf of', 'contended that', 'brought up by', 'opposition argued', 'legal submission', 'counter-argument',
	'in support of', 'submitted in defense', 'prosecution argued', 'rejected by', 'legal reasoning', 'defense pleaded', 'position of', 'argued for dismissal',
	'legal position taken', 'highlighted issues', 'presented facts', 'challenged decision', 'disputed claim', 'position taken by', 'presented argument',
	'brought forward argument', 'question of validity', 'defense statement', 'opposing counsel', 'put forth argument', 'asserted position', 'legal contention',
	'response to claim', 'argued that', 'defense maintained', 'presented evidence', 'argued point', 'issue of legality', 'defense submitted', 'questioned validity',
	'pointed out', 'suggested', 'question raised', 'argued in favor', 'counsel stated', 'objected to', 'raised defense', 'disputed argument', 'legal basis',
	'contended argument', 'presented legal theory', 'supported claim', 'contested evidence', 'claimed inconsistency', 'rebutted by', 'refuted claim', 'supported position',
	'claimed in argument', 'argued statute', 'interpretation questioned', 'provided explanation', 'argued law', 'counsel contended', 'defense claimed', 'countered argument',
	'opposed claim', 'emphasized defense', 'raised legal concern', 'established point', 'asserted legal position', 'emphasized claim', 'stated contention',
	'issue pointed out', 'challenged evidence', 'offered reasoning', 'defense counsel argued', 'pointed out discrepancy', 'legal claim presented', 'legal rationale',
	'raised factual argument', 'contested fact', 'emphasized legal rights', 'argued constitutional issue', 'pointed out legality', 'argued against'
]

categorical_pairs['A'] = {
    'Counsel': ['argued that', 'for the plaintiff', 'for the defendant', 'for the appellant', 'made submissions regarding', 'contended that', 'presented arguments for', 'addressed the issue of', 'submitted that', 'pleaded for', 'raised the question of', 'countered the claim of', 'supported the application of', 'disputed the findings of'],
    'Contended': ['that the provisions of', 'against the ruling of', 'in favor of', 'on the grounds of', 'based on the evidence', 'in support of', 'that the defendant', 'that the court', 'that the law', 'that the plaintiff', 'against the application of', 'that the judgment'],
    'Value': ['of the goods', 'of compensation', 'of services rendered', 'in dispute', 'of damages claimed', 'of the transaction', 'charged for', 'for tax purposes', 'for reimbursement', 'of the contract', 'involved in the case', 'of the agreement'],
    'Section': ['of the Act', 'states that', 'was cited by', 'applies to this case', 'provides for the rights of', 'was relied upon', 'was invoked by', 'that governs', 'that restricts', 'was referred to in', 'allows for', 'empowers the court to'],
    'Goods': ['delivered to', 'in dispute', 'supplied under contract', 'were sold to', 'were imported by', 'were exported to', 'were defective', 'were returned by', 'were subject to', 'were transferred to', 'were ordered by', 'were seized by the authorities'],
    'License': ['was granted to', 'was revoked by', 'was disputed by', 'was transferred to', 'was renewed by', 'was cancelled by', 'was issued under', 'was obtained by', 'was denied to', 'was applied for by', 'was approved by'],
    'Terms': ['of the agreement', 'of the contract', 'of service', 'agreed upon by', 'stipulated by the parties', 'accepted by', 'were breached by', 'were violated by', 'were amended by', 'were renegotiated', 'were extended for', 'were subject to'],
    'Under Section': ['the court has authority to', 'as per the law', 'the defendant is liable for', 'the plaintiff is entitled to', 'the appeal was filed', 'the ruling applies', 'the judgment was passed', 'the application was made', 'the rights were granted to', 'the claim was based on', 'the case falls under'],
    'Recipient': ['of goods', 'of payment', 'of compensation', 'of the service', 'of the contract', 'of the agreement', 'of the settlement', 'of the damages awarded', 'of the notice', 'of the property', 'of the rights', 'of the documents'],
    'Charge': ['of interest', 'of fraud', 'of negligence', 'was brought against', 'was filed by', 'was dismissed by', 'was substantiated by', 'was defended by', 'was based on', 'was denied by the court', 'was proven in court', 'was admitted by'],
    'Allegation': ['of fraud', 'of breach of contract', 'of negligence', 'was made against', 'was proven by', 'was denied by', 'was contested by', 'was supported by the evidence', 'was rejected by the court', 'was dismissed as unfounded', 'was sustained by the tribunal'],
    'Contention': ['that the contract', 'that the rights', 'that the agreement', 'that the judgment', 'that the ruling', 'that the application', 'that the damages', 'that the defendant', 'that the law', 'was supported by', 'was disputed by'],
}

## Ruling by lower court
categorical_phrases['LR'] = [
	'Tribunal', 'defendants', 'Judge', 'Bench', 'Division', 'trial', 'held that', 'trial court', 'the parent',
	'lower court decision', 'dismissed claim', 'ruled in favor', 'held for', 'adjudicated case', 'upheld by', 'previous ruling',
	'original judgment', 'found liable', 'decision rendered', 'dismissed by', 'previous findings', 'trial decision', 'ruled against',
	'determined by court', 'ruled in lower court', 'ruling upheld', 'trial decision', 'trial outcome', 'initial judgment', 'bench concluded',
	'court adjudicated', 'original decision', 'held liable', 'case dismissed', 'issued ruling', 'found by trial court', 'held as liable',
	'prior ruling', 'ruled with respect to', 'original judgment found', 'dismissed in part', 'decided by lower court', 'held by court',
	'decision rendered', 'bench concluded decision', 'affirmed ruling', 'dismissed proceedings', 'trial verdict', 'judgment upheld',
	'affirmed lower court decision', 'judgment rendered', 'lower court ruling', 'original trial decision', 'earlier ruling upheld',
	'prior court decision', 'bench issued ruling', 'verdict of trial', 'original judgment affirmed', 'determined by lower court',
	'lower court issued verdict', 'ruling by trial judge', 'prior judgment rendered', 'dismissed by lower bench', 'trial ruling affirmed',
	'court held judgment', 'adjudicated lower court', 'verdict delivered', 'initial ruling determined', 'court\'s decision in case',
	'found liable in trial', 'trial court issued decision', 'affirmed original decision', 'court held defendant liable', 'trial judgment rendered',
	'lower court’s judgment'
]

categorical_pairs['LR'] = {
    'Tribunal': ['held that', 'ruled in favor of', 'dismissed the claim', 'allowed the petition', 'issued an order for', 'found the defendant liable for', 'ordered the plaintiff to', 'quashed the appeal', 'upheld the lower court’s decision', 'set aside the judgment', 'remitted the case to', 'granted relief to', 'rejected the plea of', 'admitted the appeal'],
    'Defendant': ['was found guilty of', 'was acquitted of', 'was held liable for', 'was ordered to pay', 'was discharged from liability', 'was granted relief from', 'was denied compensation', 'was found not liable for', 'was granted an extension to', 'was refused permission to', 'was sentenced to', 'was found in breach of', 'was permitted to file', 'was required to produce evidence of'],
    'Judge': ['issued a ruling on', 'delivered the judgment in', 'held that', 'dismissed the appeal', 'found that', 'granted an injunction for', 'concluded that', 'observed that', 'set aside the order', 'referred the case to', 'admitted the evidence of', 'excluded the testimony of', 'found the plaintiff’s claim to be', 'declared that the defendant was', 'ruled in favor of', 'ordered the stay of'],
    'Bench': ['of three judges', 'ruled on the matter of', 'dismissed the case', 'delivered the judgment', 'was composed of', 'was unanimous in its decision', 'heard the arguments of', 'found that the appeal', 'allowed the petition for', 'rejected the plea of', 'observed that the evidence', 'granted leave to appeal', 'referred the matter back to', 'issued an interim order', 'reserved the judgment on'],
    'Trial Court': ['dismissed the case', 'found the defendant guilty', 'granted relief to the plaintiff', 'held that the evidence', 'issued a decree in favor of', 'denied the claim of', 'ruled that the plaintiff was', 'granted an interim order', 'observed that the defendant', 'quashed the appeal', 'set aside the previous judgment', 'ordered the defendant to pay', 'stayed the execution of', 'referred the matter to the higher court'],
    'Division': ['of the bench', 'ruled in favor of', 'heard the arguments on', 'allowed the appeal of', 'granted permission for', 'delivered the judgment in', 'was unanimous in its ruling', 'granted relief to', 'dismissed the claim of', 'issued an order for', 'admitted the evidence of', 'rejected the argument of', 'found that the appeal was'],
    'Held': ['that the plaintiff was', 'that the defendant was liable for', 'that the evidence was insufficient', 'that the judgment was to be set aside', 'that the appeal should be dismissed', 'that the compensation was justified', 'that the rights of the parties were', 'that the law applicable was', 'that the previous judgment was incorrect', 'that the ruling was valid', 'that the claims of the defendant were', 'that the plaintiff’s case was', 'that the arguments presented were valid'],
    'Claim': ['was dismissed', 'was allowed', 'was settled out of court', 'was partially upheld', 'was denied by the judge', 'was found to be valid', 'was rejected by the court', 'was quashed by the tribunal', 'was not admitted for hearing', 'was remitted for reconsideration', 'was contested by the defendant', 'was disputed by the plaintiff', 'was supported by the evidence'],
    'Verdict': ['was delivered by', 'in favor of the plaintiff', 'against the defendant', 'was unanimous', 'was rendered ex-parte', 'was recorded in court', 'was overturned on appeal', 'was based on the evidence presented', 'was disputed by the parties', 'was not subject to appeal', 'was upheld by the court of appeal', 'was delivered in open court', 'was read out by the judge', 'was finalized after'],
    'Evidence': ['was provided by', 'was insufficient to prove', 'was excluded by the court', 'was admitted by the judge', 'was presented by the plaintiff', 'was contested by the defendant', 'was disregarded by the tribunal', 'was considered by the jury', 'was rejected as inadmissible', 'was crucial to the case', 'was fabricated by', 'was found to be credible', 'was lacking in material facts', 'was critical in the ruling'],
}

## Statute
categorical_phrases['SS'] = [
    'Article',
	'provisions', 'provision', 'act', 'section', 'chapter', '(', 'explanation', 'commission', 'agent', 'estates', 'of service', 
	'subject to', 'deemed to', 'or tenure', 'as may be', 'the estates of', 'the purpose of this', 'in a case where', 'as may be prescribed',
	'statutory provision', 'statutory interpretation', 'governed by statute', 'as per provisions', 'section of law', 'chapter of statute', 
	'in accordance with', 'pursuant to', 'established by law', 'codified by', 'as set forth in', 'under statutory authority', 'legal obligation', 
	'established under', 'authorized by statute', 'provision under', 'as amended', 'per regulations', 'authorized by law', 'section 42',
	'under authority', 'law prescribes', 'requirements under', 'in compliance with', 'legal mandate', 'enacted by', 'governed by law', 'codified under', 
	'under the act', 'prescribed by', 'specified in', 'as defined by', 'within the framework of', 'bound by statute', 'interpreted under',
	'legal framework', 'statutory requirements', 'legislative provision', 'within jurisdiction', 'empowered by', 'established by statute', 'legal requirement',
	'section number', 'paragraph number', 'within chapter', 'authorized section', 'statutory interpretation', 'jurisdiction prescribed', 'defined under law',
	'pursuant to statute', 'mandatory compliance', 'legal requirement', 'provision laid out', 'required under law', 'statutory compliance', 'within legal framework',
	'governed by provision', 'codified requirement', 'defined legal standard', 'set forth by statute', 'legal compliance required', 'subject to statutory law',
	'mandatory under statute', 'legislative intent', 'provision enforced', 'statutory enforcement', 'legal interpretation', 'interpreted within statute',
	'defined legal terms', 'under statutory authority', 'subject to provision', 'legal authorization', 'statutory enforcement', 'legislative authority',
	'lawfully required', 'in accordance with act', 'subject to regulation', 'legal regulation'
]

categorical_pairs['SS'] = {
    'Provision': ['of the Act', 'states that', 'shall be enforced', 'was enacted for', 'provides for the right to', 'restricts the authority of', 'confers the power to', 'was cited in the judgment', 'was invoked by the parties', 'was referred to by the counsel', 'was applied to this case'],
    'Act': ['was passed in', 'applies to cases of', 'governs the rights of', 'was enacted to regulate', 'is relevant to', 'covers situations where', 'provides for penalties in', 'confers rights upon', 'was amended to include', 'has jurisdiction over', 'restricts the liability of', 'mandates the procedure for'],
    'Section': ['of the Act', 'applies to this case', 'grants the authority to', 'states the rights of', 'restricts the application of', 'was cited in the petition', 'confers power upon', 'provides for penalties in', 'governs the actions of', 'was amended to reflect', 'allows for the enforcement of', 'lays down the conditions for'],
    'Explanation': ['to the clause', 'of the section', 'was cited in the judgment', 'was interpreted by the court', 'clarifies the provisions of', 'was added by the amendment', 'to the provisions of', 'provides an exception to', 'was invoked in the appeal', 'gives clarity to the law'],
    'Commission': ['of inquiry', 'of investigation', 'was appointed by the government', 'was set up to investigate', 'was empowered to', 'was established under the Act', 'has the authority to', 'was tasked with', 'was set up under', 'submitted its findings to', 'was dissolved after', 'was mandated to'],
    'Agent': ['acting under', 'on behalf of', 'was authorized to', 'was appointed by', 'was terminated by', 'was empowered to', 'was representing', 'was held responsible for', 'was acting within the scope of', 'was not authorized to', 'was in breach of', 'was negligent in'],
    'Estates': ['under the provision', 'governed by the Act', 'were transferred to', 'were held by the State', 'were in dispute', 'were subject to inheritance', 'were managed by the executor', 'were leased to', 'were sold to', 'were confiscated by the government', 'were subject to mortgage', 'were registered in the name of', 'were declared as belonging to'],
    'Chapter': ['of the Constitution', 'contains provisions for', 'deals with the rights of', 'is relevant to the case of', 'lays down the procedure for', 'was amended to reflect', 'governs the actions of', 'restricts the authority of', 'confers powers upon', 'provides for penalties in', 'was enacted to protect', 'mandates the process for'],
    'Clause': ['of the section', 'under consideration', 'was cited in the judgment', 'was applied to the case', 'was relevant to the issue of', 'was interpreted by the court', 'provides an exception for', 'grants the authority to', 'was inserted by the amendment', 'lays down the conditions for', 'was relied upon by the parties', 'was in conflict with', 'was subject to review'],
    'Subject': ['to the conditions', 'to the provisions of', 'to the terms of the agreement', 'to the rules of the court', 'to the Act', 'to interpretation by the court', 'to the jurisdiction of the court', 'to the law of the State', 'to the approval of the tribunal', 'to the regulations of', 'to the approval of the parties'],
}

## Precedent
categorical_phrases['SP'] = [
	'v', 'Vs', 'vs', 'fact', 'SC', '&', 'conclusion', 'finding', 'SCC', 'S.C.R.', 'SCR', 'carrying', 'observed', 
	'previous ruling', 'as decided in', 'based on precedent', 'case law', 'binding precedent', 'established case', 'in prior case', 'judgment in', 
	'referenced case', 'previous decision', 'ruling in', 'legal precedent', 'case referenced', 'prior findings', 'upheld precedent', 'referenced judgment',
	'earlier case', 'decided case', 'case law referenced', 'judgment referred to', 'similar case law', 'precedent applied', 'court precedent', 'previous judgment',
	'case held in', 'ruling referenced', 'decision of', 'established legal precedent', 'precedent followed', 'cited judgment', 'affirmed by precedent',
	'legal findings', 'previous legal case', 'applied precedent', 'binding ruling', 'legal standard', 'settled law', 'authority cited', 'case upheld',
	'referenced ruling', 'judgment cited', 'in conformity with', 'established legal rule', 'following precedent', 'established standard', 'previous case relied upon',
	'precedent upheld', 'legal rule from prior case', 'applied binding precedent', 'settled legal standard', 'precedent established', 'prior decision referenced',
	'case upheld precedent', 'case law from court', 'judgment in line with precedent', 'binding legal rule applied', 'authoritative precedent', 'precedent followed in court',
	'earlier judgment followed', 'case law upheld', 'case cited as precedent', 'binding decision cited', 'prior case law applied', 'precedent established by court',
	'upheld judgment', 'legal precedent enforced', 'binding authority', 'precedent controlling case', 'earlier ruling referenced', 'binding case law applied'
]

categorical_pairs['SP'] = {
    'Court': ['held that', 'ruled in favor of', 'decided that', 'concluded that', 'found that the plaintiff', 'ruled against the defendant', 'stated that the law', 'determined that the evidence', 'found in favor of', 'granted relief to', 'rejected the appeal of', 'set aside the judgment of', 'quashed the decision of', 'overturned the ruling of', 'reversed the finding of', 'upheld the ruling of'],
    'Law': ['as stated by', 'as laid down in', 'is applied to', 'governs the issue of', 'was cited in the judgment', 'was interpreted by the court', 'provides for the rights of', 'restricts the authority of', 'mandates the procedure for', 'confers power upon', 'is relevant to the case of', 'was amended to reflect'],
    'Decision': ['was precedent for', 'was followed in', 'was overturned in', 'was set aside by', 'was upheld by', 'was quashed by', 'was relied upon in', 'was subject to appeal in', 'was applied to the case of', 'was used as a reference in', 'was based on the evidence of', 'was disputed by the parties'],
    'Ruling': ['of the Supreme Court', 'of this Court', 'in the previous case', 'was used as precedent', 'was upheld by the lower court', 'was challenged by the defendant', 'was contested by the plaintiff', 'was applied to the case', 'was followed by the court', 'was overturned by the appellate court', 'was questioned by the counsel', 'was cited as authority in'],
    'Finding': ['of the Court', 'was based on the evidence', 'was challenged by the plaintiff', 'was disputed by the defendant', 'was upheld by the appellate court', 'was reversed by the higher court', 'was set aside on appeal', 'was recorded in the judgment', 'was admitted by the court', 'was rejected by the tribunal', 'was relevant to the case of', 'was subject to review by'],
    'Precedent': ['set by the court in', 'was followed in the case of', 'was distinguished in', 'was applied to the facts of', 'was overruled by the appellate court', 'was upheld by the Supreme Court', 'was subject to challenge in', 'was relevant to the issue of', 'was used as authority for', 'was cited by the counsel', 'was not followed in', 'was considered binding in'],
    'Held': ['that the issue of', 'that the law applies to', 'that the judgment was correct', 'that the appeal should be dismissed', 'that the evidence was insufficient', 'that the plaintiff was entitled to', 'that the defendant was liable for', 'that the ruling was valid', 'that the previous judgment was incorrect', 'that the case was subject to'],
    'Question': ['of law', 'of fact', 'decided by the court', 'was subject to appeal', 'was referred to the tribunal', 'was raised by the plaintiff', 'was challenged by the defendant', 'was resolved by the appellate court', 'was subject to judicial review', 'was considered by the Supreme Court', 'was relevant to the case of'],
    'Case': ['of similar facts', 'was referenced in the ruling of', 'was distinguished from', 'was applied to the facts of', 'was used as precedent in', 'was subject to appeal in', 'was cited by the counsel', 'was relied upon by the plaintiff', 'was relevant to the issue of', 'was dismissed by the lower court', 'was reversed by the appellate court'],
    'Judgment': ['in the earlier case', 'serves as precedent for', 'was followed in the case of', 'was overturned on appeal', 'was set aside by the appellate court', 'was upheld by the Supreme Court', 'was cited as authority in', 'was subject to review by', 'was relied upon by the counsel', 'was distinguished in the case of'],
}

categorical_phrases['R'] = [
	'Dismiss', 'dismissed', 'dismissing', 'sustained', 'rejected', 'allowed', 'passed', 'set aside', 'quashed', 'overturned', 'affirmed',
	'appeal allowed', 'decision upheld', 'denied', 'found in favor', 'granted relief', 'dismissed with prejudice', 'ruled against', 'appeal denied',
	'judgment passed', 'motion denied', 'claim upheld', 'order vacated', 'motion granted', 'appeal dismissed', 'remanded', 'denied relief', 
	'appeal quashed', 'ruling overturned', 'appeal sustained', 'order affirmed', 'appeal ruled in favor', 'decision reversed', 'appeal found valid',
	'case dismissed', 'appeal allowed', 'ruling passed', 'order overturned', 'decree issued', 'claim granted', 'motion for reconsideration denied',
	'appeal found', 'ruling found in favor', 'granted injunction', 'judgment on claim', 'appeal quashed', 'decision stayed', 'decision in favor of',
	'ruling denied', 'judgment for respondent', 'appeal remanded', 'claim denied', 'ruling stayed', 'order in favor of', 'remanded for reconsideration', 
	'judgment passed with conditions', 'appeal dismissed with costs', 'granted leave to appeal', 'motion to dismiss denied', 'order issued', 'appeal found merit',
	'granted costs', 'final judgment issued', 'order granted', 'order issued by court', 'appeal ruling found', 'denied appeal with prejudice', 
	'remand for new trial', 'found judgment in favor', 'appeal upheld'
]

categorical_pairs['R'] = {
    'Dismissed': ['the appeal', 'the petition', 'the claim', 'the application', 'the case', 'the motion for', 'the writ filed by', 'the arguments presented by', 'the objections raised by', 'the revision petition', 'the interlocutory application'],
    'Sustained': ['the decision of', 'the lower court ruling', 'the conviction of', 'the judgment passed by', 'the objections of', 'the ruling on', 'the penalty imposed by', 'the findings of', 'the conclusion reached by', 'the orders of the tribunal'],
    'Rejected': ['the claim of', 'the application for', 'the petition filed by', 'the arguments presented by', 'the relief sought by', 'the objections of', 'the appeal made by', 'the motion to', 'the interlocutory petition', 'the writ application', 'the review petition'],
    'Allowed': ['the appeal', 'the petition', 'the claim for damages', 'the interlocutory application', 'the writ petition', 'the motion for reconsideration', 'the revision petition', 'the review petition', 'the application for interim relief', 'the objections of'],
    'Passed': ['a decree in favor of', 'an order for execution of', 'a judgment on', 'an order allowing the', 'a final ruling on', 'an interim order regarding', 'a decision on the application of', 'a writ for', 'a stay order against', 'a ruling for the plaintiff', 'a settlement order'],
    'Set Aside': ['the lower court ruling', 'the conviction of', 'the penalty imposed on', 'the decision of the tribunal', 'the judgment passed by', 'the final ruling', 'the orders of the tribunal', 'the previous order', 'the decree granted by', 'the award issued by'],
    'Considered': ['the arguments of', 'the evidence presented by', 'the appeal filed by', 'the objections raised by', 'the petition for review', 'the application for leave', 'the request for an adjournment', 'the claims made by', 'the rights of the parties involved', 'the provisions of the Act'],
    'Judgment': ['was given in favor of', 'was passed on', 'was upheld by', 'was reversed by', 'was set aside by', 'was issued by', 'was confirmed by', 'was overturned on appeal', 'was stayed by the higher court', 'was referred back to the lower court', 'was contested by the parties'],
    'Order': ['was passed to', 'for execution of', 'for dismissal of', 'was issued for', 'was vacated by the court', 'was stayed by the higher court', 'was granted for', 'was refused for', 'was made in favor of', 'was quashed by'],
    'Appeal': ['was allowed', 'was dismissed', 'was rejected', 'was granted', 'was remitted for reconsideration', 'was admitted by the court', 'was withdrawn by the parties', 'was settled out of court', 'was quashed by the tribunal', 'was contested by the defendant'],
}

for category, phrases in categorical_phrases.items():
    categorical_phrases[category] = add_case_variations(phrases)
    
updated_categorical_pairs = update_pairs_with_case_variations(categorical_pairs)

categorical_pairs = updated_categorical_pairs
