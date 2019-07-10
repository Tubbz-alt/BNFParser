import re, settings

# list of expression name - regex tuples
# expressions are extending the standard bnf
standard_exprs = []

def test_expr(regex, list):
    compiled = re.compile(regex)
    for item in list:
        matched = compiled.match(item)
        while matched:
            pos = matched.end()
            print(matched.group(0))
            matched = compiled.match(item, pos)


def phone_expr():
    # https://www.allareacodes.com/international_dialing_codes.htm
    # https://bs.wikipedia.org/wiki/Spisak_pozivnih_brojeva_u_Bosni_i_Hercegovini/
    int_code = "((00(1|11|5|[7-9])?)|(01[1-4])|(119|8|810))"
    country_code = "((\\d{1,3}))"
    nat_prefix = "(0|1|8|(0(1|5|6|7|9|82)))"
    nat_prefix_int = "((1|[5-9]|82)?)"
    number = "(\\d{0,15})"

    opt_space = "( ?)"
    opt_slash = "([/]?)"
    opt_dash = "([\\-]?)"
    opt_space_or_slash = "[ /]?"
    opt_space_or_dash = "[ \\-]?"

    plus = "+"
    opt_bracket_left = "[(]?"
    opt_bracket_right = "[)]?"

    int_call = "(" + int_code + country_code + opt_space + nat_prefix_int +  opt_space + number + ")"
    local_call = "(" + nat_prefix + number + ")"


    # BiH numbers with optional delimiters
    bih_block_1_rs = "(5[0-9])"
    bih_block_1_brcko = "(49)"
    bih_block_1_fbih = "(3[0-9])"
    bih_block_1_mobile = "(6[0-6])"
    bih_block_1 = "(" + bih_block_1_rs + "|" + bih_block_1_brcko + "|" + bih_block_1_fbih + "|" + bih_block_1_mobile + ")"
    bih_block_2 = "(\\d{3})"
    bih_block_3 = "(\\d{3,4})"

    int_and_country_code_bih = "((00|[+])387)"
    int_and_country_code_bih_opt = "(" + int_and_country_code_bih + "?" + ")"
    nat_prefix_bih = "([(]?0[)]?)?"
    nat_prefix_bih_no_brackets = "0"
    nat_prefix_bih_opt = "(" + nat_prefix_bih + "|" + nat_prefix_bih_no_brackets + ")?"

    int_call_bih = "(" + int_and_country_code_bih + opt_space + nat_prefix_bih + bih_block_1 + opt_space_or_slash + bih_block_2 + opt_space_or_dash + bih_block_3 + ")"
    local_call_bih = "((" + nat_prefix_bih_no_brackets + bih_block_1 + opt_space_or_slash + ")?" + bih_block_2 + opt_space_or_dash + bih_block_3 + ")"
    bih_call = int_call_bih + "|" + local_call_bih

    # numbers = []
    # numbers.append("00387 (0)51 123 123")
    # numbers.append("00387 51 123 123")
    # numbers.append("00387(0)51/123-123")
    # numbers.append("00387 65123123")
    # numbers.append("065/123-123")
    # numbers.append("051/123-123")
    # numbers.append("123-123")

    # test_expr(bih_call, numbers)


    phone_regex = int_call + "|" + local_call + "|" + bih_call

    global standard_exprs
    standard_exprs.append(["broj_telefona", phone_regex])


def mail_expr():
    # https://en.wikipedia.org/wiki/Email_address#Syntax
    alphanum = "[a-zA-Z0-9]"
    printable = "[!#$%&'*+-/=?^_`{|}~]"

    local_part = "(((" + alphanum + ")+[.])*(" + alphanum + ")+)"
    domain = "([a-zA-Z0-9]+[a-zA-Z0-9\\-]*[a-zA-Z\\-][a-zA-Z0-9\\-]*[a-zA-Z0-9])"
    mail_regex = local_part + "@" + domain

    # mails = []
    # mails.append("ninagrahovac.96@gmail.com")
    # mails.append("0a.00@0---000.com")
    # mails.append("0a.00@0a-00.com")
    # test_expr(mail_expr_regex, mails)

    global standard_exprs
    standard_exprs.append(["mejl_adresa", mail_regex])


def link_expr():
    # https://en.wikipedia.org/wiki/URL
    # URI = scheme + ":" + opt_authority + path + opt_query + opt_fragment

    # begins w/ lowercase letters followed by combo of letters, digits, +.-
    scheme = "[a-z][a-z0-9+.\\-]*:"

    # authority = [userinfo@]host[:port]

    # no username:password
    userinfo_base = "([a-z0-9]+)"
    opt_userinfo = "(" + userinfo_base + "@)?"

    # TODO: include IPv4/6 address
    host = "([a-z0-90.]+)"

    # TODO: fix port range
    opt_port = "(:[0-9]+)?"

    authority_base = "(" + opt_userinfo + host + opt_port + ")"
    opt_authority = "(\\/\\/" + authority_base + ")?"

    # if there is authority, must either be empty or begin with a slash
    # if no authority, cannot begin with //

    segment = "([a-zA-Z0-9]*)"
    path = "(((" + segment + ")\\/)*((" + segment + ")))?"

    # TODO: update
    query_base = "([a-z]+)"
    opt_query = "(\\?" + query_base + ")?"

    opt_fragment = "(#[a-zA-Z0-9\\-]+)?"

    URI_regex = scheme + opt_authority + path + opt_query + opt_fragment

    # links = []
    # links.append("https://www.wikipedia.org/test/")
    # links.append("https://www.wikipedia.org:1542")
    # links.append("https://regex101.com/r/25Xcyo/2")
    # links.append("https://en.wikipedia.org/wiki/URL#CITEREFBerners-Lee1994")
    # test_expr(URI_regex, links)

    global standard_exprs
    standard_exprs.append(["web_link",  URI_regex])


def num_const_expr():
    sign = "((\\+|-)?)"
    num_int = "(([1-9][0-9]+)|([0-9]))"
    num_dec = "([0-9]+[.][0-9]*[1-9][0-9]*)"
    num_regex = "(" + sign + "(" + num_dec + "|" + num_int + "))"

    # numbers = []
    # numbers.append("123")
    # numbers.append("-0123")
    # numbers.append("1.23")
    # numbers.append("0.0000000000")
    # numbers.append("-0.0000000010")
    # numbers.append("1.1.1")
    # test_expr(num_regex, numbers)

    global standard_exprs
    standard_exprs.append(["brojevna_konstanta",  num_regex])


def big_city_expr():
    with open(settings.CITIES_FILENAME) as cities_file:
        cities = cities_file.readlines()

    cities_count = len(cities)
    city_regex = "("
    for i in range(cities_count):
        if i == (cities_count - 1):
            city = cities[i]
            city_regex += city
        else:
            city = cities[i][0:-1]
            city_regex += city + "|"
        
    city_regex = city_regex + ")"
    global standard_exprs
    standard_exprs.append(["veliki_grad", city_regex])


def make_standard_exprs():
    phone_expr()
    mail_expr()
    link_expr()
    num_const_expr()
    big_city_expr()

    return standard_exprs


# big_city_expr()
