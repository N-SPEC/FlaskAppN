from flask_sqlalchemy  import SQLAlchemy

# app.py

from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)
    
app.config['SECRET_KEY'] = "dinuchakedi"

# sqlite config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'localhost:5432'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/flaskpostgre'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the instance to the 'app.py' Flask application
db = SQLAlchemy(app)
    

class area(db.Model):
    __tablename__ = 'area' 
    area_id = db.Column(db.Integer, primary_key = True)
    area_name = db.Column(db.String(250))

    def __repr__(self):
    
        return '\n area_id: {0} area_name: {1}'.format(self.area_id, self.area_name)


    def __str__(self):

        return '\n area_id: {0} area_name: {1}'.format(self.area_id, self.area_name)

class position(db.Model):
    __tablename__ = 'position' 
    position_id = db.Column(db.Integer, primary_key = True)
    area_id = db.Column(db.Integer)
    position_name = db.Column(db.String(250))

    def __repr__(self):
    
        return '\n position_id: {0} area_id: {1} position_name: {2}'.format(self.position_id, self.area_id, self.position_name)


    def __str__(self):

        return '\n position_id: {0} area_id: {1} position_name: {2}'.format(self.position_id, self.area_id, self.position_name)


def get_dropdown_values():

    area_records = area.query.all()
    # Create an empty dictionary
    myDict = {}
    for p in area_records:
    
        key = p.area_name
        area_id = p.area_id

        q = position.query.filter_by(area_id=area_id).all()
    
        lst_c = []
        for c in q:
            lst_c.append( c.position_name )
        myDict[key] = lst_c
    
    class_entry_relations = myDict
                        
    return class_entry_relations

@app.route("/area")
def show_area():
    updated_values = get_dropdown_values()
    area = updated_values.keys()
    # Create a table with HTML
    table_html = "<table><tr><th>Areas</th></tr>"
    for area in area:
        table_html += f"<tr><td>{area}</td></tr>"
    table_html += "</table>"
    return table_html

@app.route("/position")
def show_position():
    updated_values = get_dropdown_values()  # This should return a dict like {'area1': ['position1', 'position2'], 'area2': ['position3', 'position4']}
    
    # Start the HTML for the table
    table_html = "<table border='1'><tr><th>Positions</th></tr>"
    
    # Loop through the dictionary and add each position as a new row
    for position in updated_values.values():
        for position in position:
            table_html += f"<tr><td>{position}</td></tr>"
    
    table_html += "</table>"
    return table_html

@app.route('/_update_dropdown')
def update_dropdown():

    # the value of the first dropdown (selected by the user)
    selected_class = request.args.get('selected_class', type=str)

    # get values for the second dropdown
    updated_values = get_dropdown_values()[selected_class]

    # create the value sin the dropdown as a html string
    html_string_selected = ''
    for entry in updated_values:
        html_string_selected += '<option value="{}">{}</option>'.format(entry, entry)

    return jsonify(html_string_selected=html_string_selected)


@app.route('/_process_data')
def process_data():
    selected_class = request.args.get('selected_class', type=str)
    selected_entry = request.args.get('selected_entry', type=str)

    # process the two selected values here and return the response; here we just create a dummy string

    return jsonify(random_text="You selected the area: {} and the position: {}.".format(selected_class, selected_entry))




@app.route('/area_position')
def index():

    """
    initialize drop down menus
    """

    class_entry_relations = get_dropdown_values()

    default_classes = sorted(class_entry_relations.keys())
    default_values = class_entry_relations[default_classes[0]]

    return render_template('index.html',
                       all_classes=default_classes,
                       all_entries=default_values)


if __name__ == '__main__':

    app.run(debug=True, port=5001)
