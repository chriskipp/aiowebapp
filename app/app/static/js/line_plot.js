// Sample dataset. In a real application, you will probably get this data from another source such as AJAX.
var dataset = [5, 10, 15, 20, 25]

// Sizing variables for our chart. These are saved as variables as they will be used in calculations.
var chartWidth = 300
var chartHeight = 100
var padding = 5

// We want our our bars to take up the full height of the chart, so, we will apply a scaling factor to the height of every bar.
var heightScalingFactor = chartHeight / getMax(dataset)

// Here we are creating the SVG that will be our chart.
var svg = d3
  .select('#main')           // I'm starting off by selecting the container.
    .append('svg')               // Appending an SVG element to that container.
    .attr('width', chartWidth)   // Setting the width of the SVG.
    .attr('height', chartHeight) // And setting the height of the SVG.

// The next step is to create the rectangles that will make up the bars in our bar chart.
svg
  .selectAll('rect')                                          // I'm selecting all of the rectangles in the SVG (note that at this point, there actually aren't any, but we'll be creating them in a couple of steps).
  .data(dataset)                                              // Then I'm mapping the dataset to those rectangles.
  .enter()                                                    // This step is important in that it allows us to dynamically create the rectangle elements that we selected previously.
    .append('rect')                                           // For each element in the dataset, append a new rectangle.
      .attr('x', function (value, index) {                    // Set the X position of the rectangle by taking the index of the current item we are creating, multiplying it by the calculated width of each bar, and adding a padding value so we can see some space between bars.
          return (index * (chartWidth / dataset.length)) + padding
        })
      .attr('y', function (value, index) {                    // Set the rectangle by subtracting the scaled height from the height of the chart (this has to be done becuase SVG coordinates start with 0,0 at their top left corner).
        return chartHeight - (value * heightScalingFactor)
      })
      .attr('width', (chartWidth / dataset.length) - padding) // The width is dynamically calculated to have an even distribution of bars that take up the entire width of the chart.
      .attr('height', function (value, index) {               // The height is simply the value of the item in the dataset multiplied by the height scaling factor.
        return value * heightScalingFactor
      })
      .attr('fill', 'pink')                                   // Sets the color of the bars.

/**
 *  Gets the maximum value in a collection of numbers.
 */
function getMax(collection) {
  var max = 0

  collection.forEach(function (element) {
    max = element > max ? element : max
  })

  return max
}
 
