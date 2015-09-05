def main():
    from site_checker import SiteChecker
    import config
    sc = SiteChecker(config)
    sc.start()

if __name__ == "__main__":
    main()
