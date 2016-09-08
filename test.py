from parser import LmlParser

def test_happy_cases():
    print '---------- happy cases ----------\n'

    src = '    { key = this is a string}   '
    dst = LmlParser(src).parse()
    print 'src: %s\ndst: %s\n' % (src, dst)

    src = '{key1=this is a string, key2={s=   this is another string}}'
    dst = LmlParser(src).parse()
    print 'src: %s\ndst: %s\n' % (src, dst)

    src = '{track={inside2={inside3=value3}}, inside1=value1}'
    dst = LmlParser(src).parse()
    print 'src: %s\ndst: %s\n' % (src, dst)

    src = '{track={inside2={inside3=value3}}, inside1=value1,}'
    dst = LmlParser(src).parse()
    print 'src: %s\ndst: %s\n' % (src, dst)

def test_bitch_cases():
    print '---------- bitch cases ----------\n'

    src = '{abcd'
    print 'src: %s' % src
    try:
        LmlParser(src).parse()
    except ValueError, e:
        print e

    src = 'abcd}'
    print 'src: %s' % src
    try:
        LmlParser(src).parse()
    except ValueError, e:
        print e

    src = '{track={inside2={inside3=value3}, inside1=value1}'
    print 'src: %s' % src
    try:
        LmlParser(src).parse()
    except ValueError, e:
        print e


if __name__ == '__main__':
    test_happy_cases()
    print
    test_bitch_cases()
