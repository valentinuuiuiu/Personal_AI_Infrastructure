module.exports = function(eleventyConfig) {
    // Return your Object options:
    return {
      dir: {
        input: "posts",
        output: "_site",
        includes: "../_includes"
      }
    };
  };
