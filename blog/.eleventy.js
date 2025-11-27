module.exports = function(eleventyConfig) {
    // Return your Object options:
    return {
      dir: {
        input: ".",
        output: "_site",
        includes: "_includes",
        data: "_data"
      }
    };
  };
