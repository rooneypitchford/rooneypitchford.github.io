source "https://rubygems.org"

# GitHub Pages builds with this gem, which pins the exact Jekyll + plugin
# versions GitHub's own build servers use. Keeping the site on this gem
# (instead of a bare `jekyll` dependency) means what builds locally is what
# will build on GitHub Pages.
gem "github-pages", group: :jekyll_plugins

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data
# gem and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", :install_if => Gem.win_platform?

gem "http_parser.rb", "~> 0.6.0", :install_if => Gem.win_platform?
